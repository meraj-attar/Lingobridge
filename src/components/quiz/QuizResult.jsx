import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { Badge } from '../common/Badge';
import {
  CheckCircle2,
  XCircle,
  RotateCcw,
  ArrowRight,
  Trophy,
  AlertCircle,
  BookOpen
} from 'lucide-react';

export const QuizResult = ({
  result,
  onRetry,
  onNextLesson,
  onBackToCourse
}) => {
  const { score, total_questions, percentage, passed, breakdown = [] } = result;

  useEffect(() => {
    if (passed) {
      // Fire festive celebration confetti
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch (e) {
        // Fallback gracefully if canvas is blocked
      }
    }
  }, [passed]);

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in zoom-in-95 duration-300">
      {/* Result Hero Banner */}
      <Card
        className={`text-center p-8 border-2 ${
          passed
            ? 'bg-gradient-to-b from-emerald-50 to-white border-emerald-300 shadow-glow'
            : 'bg-gradient-to-b from-rose-50 to-white border-rose-300'
        }`}
      >
        <div
          className={`w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-sm ${
            passed ? 'bg-emerald-600 text-white' : 'bg-rose-600 text-white'
          }`}
        >
          {passed ? <Trophy className="w-8 h-8" /> : <AlertCircle className="w-8 h-8" />}
        </div>

        <h2 className="text-2xl font-black text-slate-900 mb-1">
          {passed ? 'Outstanding Job! You Passed!' : 'Keep Going! Review & Try Again'}
        </h2>
        <p className="text-xs text-slate-500 max-w-md mx-auto mb-6">
          {passed
            ? 'You scored above the 70% threshold. This lesson has been marked as complete in your learning records.'
            : 'You need at least 70% to pass this quiz. Review the breakdown below and attempt again.'}
        </p>

        {/* Score Pill */}
        <div className="inline-flex items-center gap-6 p-4 rounded-2xl bg-white border border-slate-200/80 shadow-soft mb-6">
          <div>
            <p className="text-[10px] uppercase font-bold text-slate-400">Score</p>
            <p className="text-2xl font-black text-slate-900">{score} / {total_questions}</p>
          </div>
          <div className="h-8 w-px bg-slate-200" />
          <div>
            <p className="text-[10px] uppercase font-bold text-slate-400">Accuracy</p>
            <p className={`text-2xl font-black ${passed ? 'text-emerald-600' : 'text-rose-600'}`}>
              {percentage}%
            </p>
          </div>
          <div className="h-8 w-px bg-slate-200" />
          <div>
            <p className="text-[10px] uppercase font-bold text-slate-400">Result</p>
            <Badge variant={passed ? 'success' : 'danger'} size="lg">
              {passed ? 'PASSED' : 'NEEDS PRACTICE'}
            </Badge>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button onClick={onRetry} variant="secondary" icon={RotateCcw}>
            Retake Quiz
          </Button>
          {onNextLesson && passed && (
            <Button onClick={onNextLesson} variant="primary" icon={ArrowRight}>
              Next Lesson
            </Button>
          )}
          <Button onClick={onBackToCourse} variant="outline" icon={BookOpen}>
            Back to Course
          </Button>
        </div>
      </Card>

      {/* Detailed Answers Review Breakdown */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <span>Question Review & Explanations</span>
          <Badge variant="default" size="sm">{breakdown.length} questions</Badge>
        </h3>

        <div className="space-y-3">
          {breakdown.map((item, idx) => (
            <Card
              key={item.question_id || idx}
              className={`border p-5 ${
                item.is_correct ? 'border-emerald-200 bg-emerald-50/20' : 'border-rose-200 bg-rose-50/20'
              }`}
            >
              <div className="flex items-start gap-3">
                <div className="mt-0.5 shrink-0">
                  {item.is_correct ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                  ) : (
                    <XCircle className="w-5 h-5 text-rose-500" />
                  )}
                </div>

                <div className="space-y-2 flex-1">
                  <div className="flex items-baseline justify-between gap-2">
                    <p className="text-sm font-bold text-slate-900 font-devanagari">
                      {idx + 1}. {item.question_text}
                    </p>
                    <Badge variant={item.is_correct ? 'success' : 'danger'} size="sm">
                      {item.is_correct ? 'Correct' : 'Incorrect'}
                    </Badge>
                  </div>

                  {/* Explanation */}
                  {item.explanation && (
                    <div className="p-3 bg-white rounded-xl border border-slate-200/80 text-xs text-slate-600 leading-relaxed font-devanagari">
                      <span className="font-semibold text-slate-800">Explanation: </span>
                      {item.explanation}
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
