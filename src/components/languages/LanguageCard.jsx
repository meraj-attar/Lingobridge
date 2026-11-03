import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { ProgressBar } from '../common/ProgressBar';
import { Badge } from '../common/Badge';
import { BookOpen, ArrowRight, CheckCircle2 } from 'lucide-react';

export const LanguageCard = ({
  language,
  progress = 0,
  isEnrolled = false,
  lessonCount = 5,
  onSelect
}) => {
  return (
    <Card hover className="flex flex-col justify-between h-full group">
      <div>
        {/* Top Flag & Status */}
        <div className="flex items-start justify-between mb-4">
          <div className="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-center text-3xl shadow-sm group-hover:scale-110 transition-transform">
            {language.flag || '🌐'}
          </div>
          {isEnrolled ? (
            <Badge variant="success" size="sm">
              <CheckCircle2 className="w-3 h-3 text-emerald-600" />
              Enrolled
            </Badge>
          ) : (
            <Badge variant="primary" size="sm">
              {language.code?.toUpperCase()}
            </Badge>
          )}
        </div>

        {/* Title & Native Name */}
        <h3 className="text-lg font-bold text-slate-900 group-hover:text-brand-600 transition-colors">
          {language.name}
        </h3>
        <p dir={language.code === 'ur' ? 'rtl' : 'ltr'} lang={language.code} className="text-xs font-semibold text-slate-400 mb-2 font-devanagari">
          {language.native_name}
        </p>

        {/* Description */}
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2 mb-4">
          {language.description || 'Learn vocabulary, grammar rules, and daily conversations.'}
        </p>
      </div>

      <div className="pt-4 border-t border-slate-100 space-y-3">
        {/* Metadata */}
        <div className="flex items-center justify-between text-xs text-slate-500 font-medium">
          <span className="inline-flex items-center gap-1">
            <BookOpen className="w-3.5 h-3.5 text-slate-400" />
            {lessonCount} {lessonCount === 1 ? 'Lesson' : 'Lessons'}
          </span>
          {isEnrolled && <span>{progress}% complete</span>}
        </div>

        {isEnrolled && (
          <ProgressBar progress={progress} size="sm" color={progress >= 100 ? 'emerald' : 'brand'} />
        )}

        <Button
          onClick={() => onSelect(language)}
          variant={isEnrolled ? 'primary' : 'outline'}
          size="sm"
          className="w-full justify-between"
        >
          <span>{isEnrolled ? 'Continue Course' : 'Start Learning'}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Button>
      </div>
    </Card>
  );
};
