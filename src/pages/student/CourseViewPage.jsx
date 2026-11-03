import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useLearning } from '../../contexts/LearningContext';
import { api } from '../../services/api';
import { LessonCard } from '../../components/lessons/LessonCard';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { ProgressBar } from '../../components/common/ProgressBar';
import { LoadingState } from '../../components/common/LoadingState';
import { EmptyState } from '../../components/common/EmptyState';
import {
  Globe,
  ArrowLeft,
  BookOpen,
  Sparkles,
  Trophy,
  CheckCircle2,
  Play
} from 'lucide-react';

export const CourseViewPage = () => {
  const { code } = useParams();
  const navigate = useNavigate();
  const {
    languages,
    levels,
    allLessons,
    enrolledLanguages,
    enrolledCourses,
    courses,
    enrollCourse,
    getLanguageProgress,
    isLessonCompleted,
    isLessonInProgress,
    getLessonQuizBestScore,
    isLoading
  } = useLearning();

  const [selectedLevelId, setSelectedLevelId] = useState('');
  const [enrollError,setEnrollError] = useState('');
  const [courseModules,setCourseModules]=useState({});
  const levelCourses=courses.filter(c=>c.language_id===languages.find(l=>l.code===code||l.id===code)?.id && c.level_id===selectedLevelId);
  useEffect(()=>{
    let live=true;
    Promise.all(levelCourses.map(c=>api.getModules(c.id).then(mods=>[c.id,mods]))).then(entries=>{if(live)setCourseModules(Object.fromEntries(entries))}).catch(e=>{if(live)setEnrollError(e.message)});
    return ()=>{live=false};
  },[code,languages,selectedLevelId,courses]);

  // Find the targeted language by code or ID
  const language = languages.find(l => l.code === code || l.id === code);

  useEffect(() => {
    if (levels.length > 0 && !selectedLevelId) {
      setSelectedLevelId(levels[0].id); // Default to A1
    }
  }, [levels, selectedLevelId]);

  if (isLoading) {
    return <LoadingState fullPage message="Loading course curriculum..." />;
  }
  if (!language) {
    return <Card className="p-8 text-center">Course not found. <Link to="/languages" className="text-brand-600 underline">Browse languages</Link></Card>;
  }

  const overallProgress = getLanguageProgress(language.id);
  const isEnrolled=enrolledCourses.some(e=>e.language_id===language.id);
  const handleEnroll=async id=>{try{setEnrollError('');await enrollCourse(id)}catch(e){setEnrollError(e.message)}};

  // Filter published lessons for this language and selected level
  const lessonsForLevel = allLessons
    .filter(l => l.language_id === language.id && l.level_id === selectedLevelId && l.is_published)
    .sort((a, b) => a.lesson_order - b.lesson_order);

  // Find first incomplete lesson to recommend
  const nextIncompleteLesson = lessonsForLevel.find(l => !isLessonCompleted(l.id)) || lessonsForLevel[0];

  const selectedLevelObj = levels.find(lvl => lvl.id === selectedLevelId);

  return (
    <div dir={language.code === 'ur' ? 'rtl' : 'ltr'} lang={language.code} className="space-y-8 pb-12">
      {/* Back to Dashboard Breadcrumb */}
      <div className="flex items-center justify-between">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
      </div>

      {/* Language Hero Header Banner */}
      <Card className="p-6 sm:p-8 bg-gradient-to-r from-white via-slate-50 to-brand-50/40 border-2 border-brand-100 shadow-soft">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="flex items-center gap-5">
            <div className="w-20 h-20 rounded-3xl bg-white border border-slate-200/80 flex items-center justify-center text-5xl shadow-sm shrink-0">
              {language.flag || '🌐'}
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <Badge variant="primary" size="sm">{language.code?.toUpperCase()}</Badge>
                <Badge variant="default" size="sm">CEFR Curriculum</Badge>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900">
                {language.name} Course
              </h1>
              <p className="text-sm font-semibold text-slate-500 font-devanagari">
                {language.native_name}
              </p>
            </div>
          </div>

          {/* Progress Pill */}
          <div className="w-full md:w-64 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-2">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700">
              <span>Overall Mastery</span>
              <span className="text-brand-600 font-bold">{overallProgress}%</span>
            </div>
            <ProgressBar progress={overallProgress} size="sm" color={overallProgress >= 100 ? 'emerald' : 'brand'} />
            <p className="text-[11px] text-slate-400">
              {overallProgress >= 100 ? '🎉 Course Completed!' : 'Pass quizzes with 70%+ to advance'}
            </p>
          </div>
        </div>
      </Card>

      {enrollError&&<p role="alert" className="text-sm text-red-700 bg-red-50 p-3 rounded-xl">{enrollError}</p>}
      {/* CEFR Difficulty Level Selector Tabs */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-900">Difficulty Levels</h2>
          <span className="text-xs text-slate-500">CEFR Framework Standard</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {levels.map((lvl) => {
            const isSelected = lvl.id === selectedLevelId;
            const levelLessons = allLessons.filter(
              l => l.language_id === language.id && l.level_id === lvl.id && l.is_published
            );
            return (
              <button
                key={lvl.id}
                onClick={() => setSelectedLevelId(lvl.id)}
                className={`p-3.5 rounded-2xl border text-left transition-all ${
                  isSelected
                    ? 'bg-brand-600 text-white border-brand-600 shadow-md shadow-brand-500/20 scale-[1.02]'
                    : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-base font-black ${isSelected ? 'text-white' : 'text-slate-900'}`}>
                    {lvl.code}
                  </span>
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${isSelected ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-500'}`}>
                    {levelLessons.length}
                  </span>
                </div>
                <p className={`text-xs font-semibold truncate ${isSelected ? 'text-brand-100' : 'text-slate-500'}`}>
                  {lvl.name}
                </p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Actual hierarchy: proficiency → individual courses → ordered modules → ordered lessons */}
      <div className="space-y-5">
        <h2 className="text-lg font-bold text-slate-900">{selectedLevelObj?.code} Courses</h2>
        {!levelCourses.length&&<EmptyState icon={BookOpen} title="No courses published yet" description="Choose another level or ask an administrator to publish a course." />}
        {levelCourses.map(course=>{
          const ownCourse=enrolledCourses.find(c=>c.id===course.id);
          const enrolled=!!ownCourse;
          const current=ownCourse||course;
          const modules=courseModules[course.id]||[];
          return <Card key={course.id} className="p-6 space-y-5 border-2 border-brand-100">
            <div className="flex flex-wrap justify-between items-start gap-4">
              <div><h3 className="text-xl font-black text-slate-900">{course.title}</h3><p className="text-sm text-slate-500 mt-1">{course.description}</p><p className="text-xs text-brand-700 mt-2">{current.completed_lessons} / {current.lesson_count} lessons completed</p><div className="mt-2 max-w-sm"><ProgressBar progress={current.progress_percent||0} size="sm" /></div></div>
              {enrolled?<Badge variant="success">Enrolled</Badge>:<Button onClick={()=>handleEnroll(course.id)}>Enroll in this course</Button>}
            </div>
            {!enrolled&&<p className="text-sm text-slate-500">Enrollment in this course is required before opening lessons or submitting assessments.</p>}
            {modules.map(mod=><section key={mod.id} className="space-y-3"><h4 className="font-bold text-slate-800">Module {mod.sort_order}: {mod.title}</h4>
              {mod.lessons.length?<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{mod.lessons.map(l=><LessonCard key={l.id} lesson={l} isCompleted={isLessonCompleted(l.id)} isInProgress={isLessonInProgress(l.id)} bestQuizScore={getLessonQuizBestScore(l.id)} disabled={!enrolled} onOpenLesson={id=>navigate(`/lesson/${id}`)} />)}</div>:<p className="text-xs text-slate-500">No published lessons in this module.</p>}
              {!enrolled&&<p className="text-xs text-orange-700">Enroll in this course to access its lessons.</p>}
            </section>)}
          </Card>;
        })}
      </div>
    </div>
  );
};
