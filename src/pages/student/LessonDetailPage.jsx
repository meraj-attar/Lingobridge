import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../../services/api';
import { useLearning } from '../../contexts/LearningContext';
import { VocabularyList } from '../../components/lessons/VocabularyList';
import { GrammarSection } from '../../components/lessons/GrammarSection';
import { Button } from '../../components/common/Button';
import { Badge } from '../../components/common/Badge';
import { Card } from '../../components/common/Card';
import { LoadingState } from '../../components/common/LoadingState';
import {
  ArrowLeft,
  ArrowRight,
  Clock,
  HelpCircle,
  CheckCircle2,
  BookOpen,
  Sparkles,
  Award
} from 'lucide-react';

export const LessonDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isLessonCompleted, getLessonQuizBestScore, allLessons, refreshData } = useLearning();

  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [bookmarked,setBookmarked] = useState(false);
  const [bookmarkError,setBookmarkError] = useState('');
  const [startNotice,setStartNotice] = useState('');

  useEffect(() => {
    let active = true;
    const fetchLesson = async () => {
      try {
        setIsLoading(true);
        setError(null);
        setStartNotice('');
        const data = await api.getLessonById(id);
        if (!active) return;
        setLesson(data);
        api.getBookmarks().then(items=>{if(active)setBookmarked(items.some(b=>b.lesson_id===id))}).catch(()=>{});
        api.submitLessonStart(id).then(()=>refreshData()).catch(e=>{if(active)setStartNotice('Lesson opened, but progress could not be updated: '+e.message)});
      } catch (err) {
        console.error('Failed to load lesson:', err);
        if (active) setError(err.message || 'Lesson not found');
      } finally {
        if (active) setIsLoading(false);
      }
    };

    if (id) fetchLesson();
    return () => { active = false; };
  }, [id]);

  if (isLoading) {
    return <LoadingState fullPage message="Loading lesson materials..." />;
  }

  if (error || !lesson) {
    return (
      <Card className="text-center p-12 max-w-lg mx-auto">
        <h3 className="text-lg font-bold text-slate-900 mb-2">Lesson Not Found</h3>
        <p className="text-xs text-slate-500 mb-6">{error || 'This lesson does not exist or has been removed.'}</p>
        <Link to="/dashboard">
          <Button variant="primary" size="sm">Back to Dashboard</Button>
        </Link>
      </Card>
    );
  }

  const isCompleted = isLessonCompleted(lesson.id);
  const bestScore = getLessonQuizBestScore(lesson.id);

  // Find previous and next lessons within the same language and level
  const sameLevelLessons = allLessons
    .filter(l => l.module_id === lesson.module_id && l.is_published)
    .sort((a, b) => a.lesson_order - b.lesson_order);

  const currentIdx = sameLevelLessons.findIndex(l => l.id === lesson.id);
  const prevLesson = currentIdx > 0 ? sameLevelLessons[currentIdx - 1] : null;
  const nextLesson = currentIdx >= 0 && currentIdx < sameLevelLessons.length - 1 ? sameLevelLessons[currentIdx + 1] : null;

  return (
    <div dir={lesson.languages?.code === 'ur' ? 'rtl' : 'ltr'} lang={lesson.languages?.code || 'en'} className="space-y-8 pb-16 max-w-4xl mx-auto">
      {startNotice && <p role="alert" className="rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">{startNotice}</p>}
      {/* 1. Breadcrumbs */}
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-slate-500">
        <div className="flex items-center gap-2">
          <Link to="/dashboard" className="hover:text-slate-800 transition-colors">
            Dashboard
          </Link>
          <span>/</span>
          <Link
            to={`/course/${lesson.languages?.code || lesson.language_id}`}
            className="hover:text-slate-800 transition-colors font-medium text-slate-700"
          >
            {lesson.languages?.name || 'Course'}
          </Link>
          <span>/</span>
          <span className="font-semibold text-brand-600">
            {lesson.course_levels?.code || 'A1'} – Lesson #{lesson.lesson_order}
          </span>
        </div>

        <Link
          to={`/course/${lesson.languages?.code || lesson.language_id}`}
          className="inline-flex items-center gap-1 font-semibold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Course Curriculum
        </Link>
      </div>

      {/* 2. Lesson Title Header */}
      <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-soft space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{lesson.languages?.flag || '🌐'}</span>
            <Badge variant="primary" size="sm">
              {lesson.languages?.name} • {lesson.course_levels?.code}
            </Badge>
            <span className="inline-flex items-center gap-1 text-xs text-slate-500 font-medium">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              {lesson.duration_minutes || 15} mins
            </span>
          </div>

          {isCompleted ? (
            <Badge variant="success" size="md">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Completed ({bestScore}%)
            </Badge>
          ) : (
            <Badge variant="default" size="md">
              In Progress
            </Badge>
          )}
        </div>

        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight font-devanagari">
            {lesson.title}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1 leading-relaxed font-devanagari">
            {lesson.description}
          </p>
        </div>

        {/* Objectives Box */}
        {lesson.objectives && (
          <div className="bg-slate-50 rounded-2xl p-4 border border-slate-100 space-y-1.5">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-brand-600" />
              Learning Objectives
            </h4>
            <ul className="text-xs text-slate-600 space-y-1 font-devanagari">
              {Array.isArray(lesson.objectives) ? (
                lesson.objectives.map((obj, i) => <li key={i}>• {obj}</li>)
              ) : (
                <li>• {lesson.objectives}</li>
              )}
            </ul>
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3"><button className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-brand-700" onClick={async()=>{try{setBookmarkError('');if(bookmarked){await api.unbookmark(lesson.id);setBookmarked(false)}else{await api.bookmark(lesson.id);setBookmarked(true)}}catch(e){setBookmarkError(e.message)}}}>{bookmarked?'★ Saved — Remove Bookmark':'☆ Bookmark this Lesson'}</button>{bookmarkError&&<p className="text-sm text-red-600">{bookmarkError}</p>}</div>
      {/* 4. Explanatory Content & Grammar */}
      <GrammarSection grammarNotes={lesson.grammar_notes} content={lesson.content} />

      {/* 5. Vocabulary Cards */}
      <VocabularyList
        items={lesson.vocabulary_items || []}
        languageCode={lesson.languages?.code || 'en'}
      />

      {/* 6. Sticky / Prominent Quiz CTA Section */}
      <Card className="p-6 sm:p-8 bg-gradient-to-r from-brand-600 to-indigo-600 text-white shadow-soft-lg flex flex-col sm:flex-row items-center justify-between gap-6 rounded-3xl">
        <div className="space-y-1 text-center sm:text-left">
          <div className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-white/20 text-white text-[11px] font-bold">
            <Award className="w-3.5 h-3.5" />
            Knowledge Check
          </div>
          <h3 className="text-xl font-black text-white">
            Ready to test your comprehension?
          </h3>
          <p className="text-xs text-brand-100 max-w-md">
            Pass the interactive quiz with 70%+ to complete this lesson and update your learning statistics.
          </p>
        </div>

        <Button
          onClick={() => navigate(`/lesson/${lesson.id}/quiz`)}
          variant="secondary"
          size="lg"
          className="shrink-0 bg-white text-brand-700 hover:bg-slate-100 shadow-sm font-bold"
          icon={HelpCircle}
        >
          {isCompleted ? 'Retake Quiz' : 'Start Lesson Quiz'}
        </Button>
      </Card>

      {/* 7. Lesson Navigation Bottom Bar */}
      <div className="pt-6 border-t border-slate-200 flex items-center justify-between gap-4">
        {prevLesson ? (
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate(`/lesson/${prevLesson.id}`)}
            icon={ArrowLeft}
          >
            Previous: #{prevLesson.lesson_order}
          </Button>
        ) : (
          <div />
        )}

        <Link to={`/course/${lesson.languages?.code || lesson.language_id}`}>
          <Button variant="ghost" size="sm" icon={BookOpen}>
            Course Overview
          </Button>
        </Link>

        {nextLesson ? (
          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate(`/lesson/${nextLesson.id}`)}
          >
            <span>Next: #{nextLesson.lesson_order}</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
          </Button>
        ) : (
          <Button
            variant="success"
            size="sm"
            onClick={() => navigate(`/course/${lesson.languages?.code || lesson.language_id}`)}
            icon={CheckCircle2}
          >
            Complete Course
          </Button>
        )}
      </div>
    </div>
  );
};
