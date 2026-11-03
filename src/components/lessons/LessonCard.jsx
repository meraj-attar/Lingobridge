import React from 'react';
import { Card } from '../common/Card';
import { Button } from '../common/Button';
import { Badge } from '../common/Badge';
import { CheckCircle2, Clock, PlayCircle, HelpCircle, ArrowRight, Lock } from 'lucide-react';

export const LessonCard = ({
  lesson,
  isCompleted = false,
  isInProgress = false,
  bestQuizScore = null,
  disabled = false,
  onOpenLesson
}) => {
  return (
    <Card hover className="flex flex-col justify-between group">
      <div>
        {/* Header: Order & Status */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-xl bg-brand-50 text-brand-700 font-bold text-xs flex items-center justify-center border border-brand-100">
              #{lesson.lesson_order}
            </span>
            <span className="inline-flex items-center gap-1 text-xs text-slate-500 font-medium">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              {lesson.duration_minutes || 15} mins
            </span>
          </div>

          {isCompleted ? (
            <Badge variant="success" size="sm">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              Completed
            </Badge>
          ) : isInProgress ? (
            <Badge variant="warning" size="sm">
              In Progress
            </Badge>
          ) : (
            <Badge variant="default" size="sm">
              Ready
            </Badge>
          )}
        </div>

        {/* Title */}
        <h4 className="text-base font-bold text-slate-900 group-hover:text-brand-600 transition-colors mb-1.5 font-devanagari">
          {lesson.title}
        </h4>

        {/* Description */}
        <p className="text-xs text-slate-500 leading-relaxed line-clamp-2 mb-4 font-devanagari">
          {lesson.description || 'Explore this structured beginner lesson.'}
        </p>

        {/* Objectives Pill */}
        {lesson.objectives && lesson.objectives.length > 0 && (
          <div className="bg-slate-50 rounded-xl p-3 border border-slate-100 text-[11px] text-slate-600 space-y-1 mb-4">
            <span className="font-semibold text-slate-800 block">Key Goal:</span>
            <p className="line-clamp-1 italic text-slate-500 font-devanagari">
              • {Array.isArray(lesson.objectives) ? lesson.objectives[0] : lesson.objectives}
            </p>
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
        {bestQuizScore !== null ? (
          <span className="text-xs font-semibold text-emerald-600">
            Quiz Score: {bestQuizScore}%
          </span>
        ) : (
          <span className="text-xs text-slate-400 flex items-center gap-1 font-medium">
            <HelpCircle className="w-3.5 h-3.5" />
            Quiz Included
          </span>
        )}

        <Button
          onClick={() => onOpenLesson(lesson.id)}
          disabled={disabled}
          variant={isCompleted ? 'outline' : 'primary'}
          size="sm"
          className="gap-1.5"
        >
          <span>{disabled ? 'Enroll to Open' : isCompleted ? 'Review' : 'Start'}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Button>
      </div>
    </Card>
  );
};
