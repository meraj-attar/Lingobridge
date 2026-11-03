import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useLearning } from '../../contexts/LearningContext';
import { WelcomeBanner } from '../../components/dashboard/WelcomeBanner';
import { QuickStats } from '../../components/dashboard/QuickStats';
import { ContinueLearningCard } from '../../components/dashboard/ContinueLearningCard';
import { EnrolledLanguageCard } from '../../components/dashboard/EnrolledLanguageCard';
import { LessonCard } from '../../components/lessons/LessonCard';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { LoadingState } from '../../components/common/LoadingState';
import { BookOpen, Plus, Sparkles, Trophy, ArrowRight } from 'lucide-react';

export const StudentDashboard = () => {
  const navigate = useNavigate();
  const {
    languages,
    allLessons,
    enrolledLanguages,
    enrolledCourses,
    courses,
    recommendations,
    isLoading,
    getLanguageProgress,
    isLessonCompleted,
    isLessonInProgress,
    getLessonQuizBestScore,
    getRecentlyAccessedLesson
  } = useLearning();

  if (isLoading) {
    return <LoadingState fullPage message="Loading your dashboard & progress..." />;
  }

  const recentData = getRecentlyAccessedLesson();

  // Enrolled languages list with full language details
  const activeEnrolledList = enrolledLanguages.map((enr) => {
    const lang = languages.find(l => l.id === enr.language_id) || enr.languages || {};
    const progress = getLanguageProgress(lang.id);
    const langLessons = allLessons.filter(l => l.language_id === lang.id && l.is_published);
    return {
      language: lang,
      progress,
      lessonCount: langLessons.length
    };
  });

  // Recommended Lessons: find up to 3 incomplete beginner lessons
  const recommendedLessons = (recommendations.lessons || [])
    .map(item => ({ ...allLessons.find(l => l.id === item.lesson_id), reason: item.reason }))
    .filter(l => l.id && l.is_published);

  return (
    <div className="space-y-8 pb-12">
      {/* 1. Motivational Welcome Header */}
      <WelcomeBanner />

      {/* 2. Key Metrics Stats */}
      <QuickStats />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4"><Link to="/profile" className="bg-white border rounded-2xl p-4 text-brand-600 font-semibold">My Profile &amp; Goals →</Link><Link to="/flashcards" className="bg-white border rounded-2xl p-4 text-brand-600 font-semibold">Practise Flashcards · {recommendations.review_due ?? 0} due →</Link></div>
      {/* 3. Continue Learning Fast Banner */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-brand-600" />
            Jump Back In
          </h2>
        </div>
        <ContinueLearningCard recentData={recentData} />
      </div>

      {/* 4. My Languages Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900">My Languages</h2>
            <p className="text-xs text-slate-500">Track and manage your enrolled language courses</p>
          </div>
          <Link to="/languages">
            <Button variant="outline" size="sm" icon={Plus}>
              Enroll New Language
            </Button>
          </Link>
        </div>

        {activeEnrolledList.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {activeEnrolledList.map(({ language, progress, lessonCount }) => (
              <EnrolledLanguageCard
                key={language.id}
                language={language}
                progress={progress}
                lessonCount={lessonCount}
              />
            ))}
          </div>
        ) : (
          <Card className="text-center p-8 border-2 border-dashed border-slate-200">
            <BookOpen className="w-10 h-10 text-slate-400 mx-auto mb-2" />
            <h3 className="text-sm font-bold text-slate-800">You haven't enrolled in any languages yet</h3>
            <p className="text-xs text-slate-500 mb-4">Choose from all ten supported languages to get started.</p>
            <Link to="/languages">
              <Button size="sm">Browse Languages</Button>
            </Link>
          </Card>
        )}
      </div>

      <div className="space-y-3"><h2 className="text-lg font-bold">My Enrolled Courses</h2>
      {enrolledCourses.length?<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">{enrolledCourses.map(c=><Link to={`/course/${languages.find(l=>l.id===c.language_id)?.code||c.language_id}`} key={c.id} className="block bg-white rounded-2xl border p-5 hover:border-brand-300"><h3 className="font-bold">{c.title}</h3><p className="text-xs text-slate-500 mt-2">{c.completed_lessons} of {c.lesson_count} lessons completed · {c.progress_percent}%</p></Link>)}</div>:<Card className="p-5 text-sm text-slate-500">Choose a language and enroll in an individual proficiency course to begin.</Card>}
      </div>
      {/* 5. Recommended Lessons */}
      {recommendedLessons.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Recommended Lessons</h2>
              <p className="text-xs text-slate-500">Continue building your foundational vocabulary and grammar</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recommendedLessons.map((lesson) => (
              <div key={lesson.id}><p className="text-xs text-brand-700 font-semibold mb-2" aria-label="Why recommended">{lesson.reason}</p><LessonCard
                key={lesson.id}
                lesson={lesson}
                isCompleted={isLessonCompleted(lesson.id)}
                isInProgress={isLessonInProgress(lesson.id)}
                bestQuizScore={getLessonQuizBestScore(lesson.id)}
                onOpenLesson={(id) => navigate(`/lesson/${id}`)}
              /></div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
