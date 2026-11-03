import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { ProgressBar } from '../common/ProgressBar';
import { Badge } from '../common/Badge';
import { ArrowRight, BookOpen } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const EnrolledLanguageCard = ({ language, progress = 0, lessonCount = 5 }) => {
  const navigate = useNavigate();

  return (
    <Card hover className="flex flex-col justify-between h-full group">
      <div>
        <div className="flex items-start justify-between mb-4">
          <div className="w-12 h-12 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-center text-2xl shadow-sm group-hover:scale-105 transition-transform">
            {language.flag || '🌐'}
          </div>
          <Badge variant={progress >= 100 ? 'success' : 'primary'} size="sm">
            {progress >= 100 ? 'Completed' : `${progress}% Done`}
          </Badge>
        </div>

        <h3 className="text-base font-bold text-slate-900 group-hover:text-brand-600 transition-colors">
          {language.name}
        </h3>
        <p className="text-xs font-semibold text-slate-400 mb-3 font-devanagari">
          {language.native_name}
        </p>

        <div className="space-y-1.5 mb-4">
          <div className="flex justify-between text-xs text-slate-500 font-medium">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <ProgressBar progress={progress} size="sm" color={progress >= 100 ? 'emerald' : 'brand'} />
        </div>
      </div>

      <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
        <span className="text-xs text-slate-400 font-medium flex items-center gap-1">
          <BookOpen className="w-3.5 h-3.5" />
          {lessonCount} Lessons
        </span>

        <Button
          onClick={() => navigate(`/course/${language.code || language.id}`)}
          variant="outline"
          size="sm"
          className="gap-1 text-xs"
        >
          <span>Continue</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Button>
      </div>
    </Card>
  );
};
