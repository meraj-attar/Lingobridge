import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import { useAuth } from './AuthContext';

const LearningContext = createContext(null);

export const LearningProvider = ({ children }) => {
  const { user } = useAuth();
  const [languages, setLanguages] = useState([]);
  const [levels, setLevels] = useState([]);
  const [allLessons, setAllLessons] = useState([]);
  const [courses,setCourses] = useState([]);
  const [enrolledCourses,setEnrolledCourses] = useState([]);
  const [enrolledLanguages, setEnrolledLanguages] = useState([]);
  const [progress, setProgress] = useState({ lesson_progress: [], quiz_attempts: [] });
  const [recommendations, setRecommendations] = useState({ lessons: [], review_due: 0, review_total: 0 });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load baseline languages, levels, and lessons
  const loadBaseData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [langsData, levelsData, lessonsData, coursesData] = await Promise.all([
        api.getLanguages(), api.getLevels(), api.getLessons(), api.getCourses()
      ]);
      setCourses(coursesData||[]);
      setLanguages(langsData || []);
      setLevels(levelsData || []);
      setAllLessons(lessonsData || []);
    } catch (err) {
      console.error('Error loading base learning data:', err);
      setError(err.message || 'Failed to load course catalogue');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Load student-specific data
  const loadStudentData = useCallback(async () => {
    if (!user?.id) {
      setEnrolledLanguages([]);
      setEnrolledCourses([]);
      setProgress({ lesson_progress: [], quiz_attempts: [] });
      setRecommendations({ lessons: [], review_due: 0, review_total: 0 });
      return;
    }

    try {
      const [enrollments, progressData, courseItems, recommendationData] = await Promise.all([
        api.getStudentEnrollments(), api.getStudentProgress(), api.getEnrolledCourses(), api.getRecommendations()
      ]);
      setRecommendations(recommendationData||{ lessons: [], review_due: 0, review_total: 0 });
      setEnrolledCourses(courseItems||[]);
      setEnrolledLanguages(enrollments || []);
      setProgress(progressData || { lesson_progress: [], quiz_attempts: [] });
    } catch (err) {
      console.error('Error loading student progress:', err);
    }
  }, [user]);

  useEffect(() => {
    loadBaseData();
  }, [loadBaseData]);

  useEffect(() => {
    loadStudentData();
  }, [loadStudentData]);

  const refreshData = useCallback(async () => {
    await Promise.all([loadBaseData(), loadStudentData()]);
  }, [loadBaseData, loadStudentData]);

  // Enroll in language
  const enrollLanguage = async (languageId) => {
    if (!user?.id) return;
    try {
      await api.enrollInLanguage(user.id, languageId);
      await loadStudentData();
    } catch (err) {
      console.error('Error enrolling in language:', err);
      throw err;
    }
  };

  const enrollCourse = async courseId => {
    if (!user?.id) throw new Error('Sign in first');
    await api.enrollInCourse(courseId);
    await refreshData();
  };

  // Progress calculations
  const getLanguageProgress = (languageId) => {
    const publishedLangLessons = allLessons.filter(
      l => l.language_id === languageId && l.is_published
    );
    if (publishedLangLessons.length === 0) return 0;

    const completedLessonIds = progress.lesson_progress
      .filter(p => p.status === 'completed')
      .map(p => p.lesson_id);

    const completedInThisLang = publishedLangLessons.filter(l =>
      completedLessonIds.includes(l.id)
    ).length;

    return Math.min(100, Math.round((completedInThisLang / publishedLangLessons.length) * 100));
  };

  const isLessonCompleted = (lessonId) => {
    return progress.lesson_progress.some(
      p => p.lesson_id === lessonId && p.status === 'completed'
    );
  };

  const isLessonInProgress = (lessonId) => {
    return progress.lesson_progress.some(
      p => p.lesson_id === lessonId && p.status === 'in_progress'
    );
  };

  const getLessonQuizBestScore = (lessonId) => {
    const attempts = progress.quiz_attempts.filter(a => a.lesson_id === lessonId);
    if (attempts.length === 0) return null;
    return attempts.reduce((max, curr) => (curr.percentage > max ? curr.percentage : max), 0);
  };

  const getTotalCompletedLessons = () => {
    return progress.lesson_progress.filter(p => p.status === 'completed').length;
  };

  const getOverallQuizAverage = () => {
    if (!progress.quiz_attempts || progress.quiz_attempts.length === 0) return 0;
    const total = progress.quiz_attempts.reduce((sum, a) => sum + Number(a.percentage || 0), 0);
    return Math.round(total / progress.quiz_attempts.length);
  };

  const getRecentlyAccessedLesson = () => {
    // Find the first enrolled language with incomplete published lesson
    for (const course of enrolledCourses) {
      const langLessons = allLessons.filter(l => l.course_id === course.id && l.is_published);
      const nextIncomplete = langLessons.find(l => !isLessonCompleted(l.id));
      if (nextIncomplete) {
        const lang = languages.find(l => l.id === course.language_id);
        return { lesson: nextIncomplete, language: lang };
      }
    }
    // Never recommend a lesson in a course the learner has not enrolled in.
    return null;
  };

  return (
    <LearningContext.Provider
      value={{
        languages,
        levels,
        courses,
        enrolledCourses,
        enrollCourse,
        allLessons,
        enrolledLanguages,
        progress,
        recommendations,
        isLoading,
        error,
        refreshData,
        enrollLanguage,
        getLanguageProgress,
        isLessonCompleted,
        isLessonInProgress,
        getLessonQuizBestScore,
        getTotalCompletedLessons,
        getOverallQuizAverage,
        getRecentlyAccessedLesson
      }}
    >
      {children}
    </LearningContext.Provider>
  );
};

export const useLearning = () => {
  const context = useContext(LearningContext);
  if (!context) {
    throw new Error('useLearning must be used within a LearningProvider');
  }
  return context;
};
