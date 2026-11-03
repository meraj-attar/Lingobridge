import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../../services/api';
import { useLearning } from '../../contexts/LearningContext';
import { QuizRunner } from '../../components/quiz/QuizRunner';
import { LoadingState } from '../../components/common/LoadingState';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';
import { ArrowLeft, BookOpen } from 'lucide-react';

export const QuizPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { allLessons } = useLearning();

  const [lesson, setLesson] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadLessonQuiz = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await api.getLessonById(id);
        setLesson(data);
      } catch (err) {
        console.error('Failed to load quiz:', err);
        setError(err.message || 'Quiz could not be loaded');
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      loadLessonQuiz();
    }
  }, [id]);

  if (isLoading) {
    return <LoadingState fullPage message="Loading quiz questions..." />;
  }

  if (error || !lesson) {
    return (
      <Card className="text-center p-12 max-w-lg mx-auto">
        <h3 className="text-base font-bold text-slate-800 mb-2">Quiz Not Found</h3>
        <p className="text-xs text-slate-500 mb-6">{error || 'This quiz could not be loaded.'}</p>
        <Link to="/dashboard" className="text-xs font-semibold text-brand-600">
          Return to Dashboard
        </Link>
      </Card>
    );
  }

  // Find next lesson for seamless progression
  const sameLevelLessons = allLessons
    .filter(l => l.module_id === lesson.module_id && l.is_published)
    .sort((a, b) => a.lesson_order - b.lesson_order);

  const currentIdx = sameLevelLessons.findIndex(l => l.id === lesson.id);
  const nextLesson = currentIdx >= 0 && currentIdx < sameLevelLessons.length - 1 ? sameLevelLessons[currentIdx + 1] : null;

  return (
    <div className="space-y-6 pb-16 max-w-3xl mx-auto">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <Link
          to={`/lesson/${lesson.id}`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Lesson Content
        </Link>

        <div className="flex items-center gap-2">
          <Badge variant="primary" size="sm">
            {lesson.languages?.flag} {lesson.languages?.name}
          </Badge>
          <Badge variant="default" size="sm">
            Lesson #{lesson.lesson_order} Quiz
          </Badge>
        </div>
      </div>

      <div className="text-center space-y-1">
        <h1 className="text-2xl font-black text-slate-900 font-devanagari">
          {lesson.title} – Assessment
        </h1>
        <p className="text-xs text-slate-500">
          Answer all questions carefully to demonstrate your understanding.
        </p>
      </div>

      {/* Quiz Runner Engine */}
      <QuizRunner
        languageCode={lesson.languages?.code || 'en'}
        lessonId={lesson.id}
        questions={lesson.quiz_questions || []}
        onNextLesson={nextLesson ? () => navigate(`/lesson/${nextLesson.id}`) : null}
        onBackToCourse={() => navigate(`/course/${lesson.languages?.code || lesson.language_id}`)}
      />
    </div>
  );
};
