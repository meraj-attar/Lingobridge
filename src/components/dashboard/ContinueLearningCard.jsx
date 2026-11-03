import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import { PlayCircle, Clock, BookOpen, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const ContinueLearningCard = ({ recentData }) => {
  const navigate = useNavigate();

  if (!recentData || !recentData.lesson) {
    return (
      <Card className="bg-gradient-to-r from-brand-50 to-blue-50/50 border-brand-200/80 p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="space-y-1 text-center sm:text-left">
          <h3 className="text-base font-bold text-slate-900">Ready to start your first lesson?</h3>
          <p className="text-xs text-slate-500">
            Select a language from the catalogue to begin your personalized learning journey.
          </p>
        </div>
        <Button onClick={() => navigate('/languages')} size="sm" icon={BookOpen}>
          Explore Languages
        </Button>
      </Card>
    );
  }

  const { lesson, language } = recentData;

  return (
    <Card className="bg-white border-2 border-brand-100 shadow-soft-lg p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-50 rounded-bl-full -z-0 pointer-events-none" />

      <div className="relative z-10 flex items-start gap-4">
        <div className="w-14 h-14 rounded-2xl bg-brand-50 border border-brand-200 flex items-center justify-center text-3xl shrink-0 shadow-sm">
          {language?.flag || '🌐'}
        </div>

        <div className="space-y-1">
          <div className="flex items-center gap-2 flex-wrap">
            <Badge variant="primary" size="sm">
              {language?.name || 'Language'}
            </Badge>
            <Badge variant="default" size="sm">
              Lesson #{lesson.lesson_order}
            </Badge>
            <span className="inline-flex items-center gap-1 text-[11px] text-slate-400 font-medium">
              <Clock className="w-3 h-3" />
              {lesson.duration_minutes || 15} mins
            </span>
          </div>

          <h3 className="text-lg font-bold text-slate-900 font-devanagari">
            {lesson.title}
          </h3>

          <p className="text-xs text-slate-500 line-clamp-1 max-w-xl font-devanagari">
            {lesson.description}
          </p>
        </div>
      </div>

      <div className="relative z-10 w-full md:w-auto shrink-0">
        <Button
          onClick={() => navigate(`/lesson/${lesson.id}`)}
          variant="primary"
          size="md"
          className="w-full sm:w-auto"
          icon={PlayCircle}
        >
          <span>Continue Lesson</span>
          <ArrowRight className="w-4 h-4 ml-1" />
        </Button>
      </div>
    </Card>
  );
};
