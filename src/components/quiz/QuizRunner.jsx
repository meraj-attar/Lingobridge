import React, { useState, useEffect } from 'react';
import { QuizQuestion } from './QuizQuestion';
import { QuizResult } from './QuizResult';
import { ProgressBar } from '../common/ProgressBar';
import { Button } from '../common/Button';
import { Card } from '../common/Card';
import { ErrorMessage } from '../common/ErrorMessage';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext';
import { useLearning } from '../../contexts/LearningContext';
import { ArrowLeft, ArrowRight, CheckCircle2, HelpCircle } from 'lucide-react';

export const QuizRunner = ({
  lessonId,
  languageCode = 'en',
  questions = [],
  onNextLesson,
  onBackToCourse
}) => {
  const { user } = useAuth();
  const { refreshData } = useLearning();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // { [question_id]: option_id }
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [attemptToken,setAttemptToken] = useState(null);
  const [secondsLeft,setSecondsLeft] = useState(null);
  const [sessionReady,setSessionReady] = useState(false);
  const begin = async () => {
    setSessionReady(false);
    try{const data=await api.beginQuiz(lessonId);setAttemptToken(data.attempt_token);setSecondsLeft(data.limit_seconds||null);setError(null);}
    catch(e){setError(e.message);}
    finally{setSessionReady(true);}
  };
  useEffect(()=>{begin();},[lessonId]);
  useEffect(()=>{if(secondsLeft===null||secondsLeft<=0||result)return;
    const timer=setTimeout(()=>setSecondsLeft(x=>x===null?null:Math.max(0,x-1)),1000);
    return ()=>clearTimeout(timer);
  },[secondsLeft,result]);

  if (!questions || questions.length === 0) {
    return (
      <Card className="text-center p-12 max-w-lg mx-auto">
        <HelpCircle className="w-12 h-12 text-slate-400 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800 mb-1">No Quiz Questions Available</h3>
        <p className="text-xs text-slate-500 mb-6">
          The instructor has not added quiz questions to this lesson yet.
        </p>
        <Button onClick={onBackToCourse} variant="outline" size="sm">
          Return to Course
        </Button>
      </Card>
    );
  }

  const currentQuestion = questions[currentIndex];
  const totalQuestions = questions.length;
  const progressPercent = Math.round(((currentIndex + 1) / totalQuestions) * 100);
  const selectedOptionId = answers[currentQuestion.id];
  const isLastQuestion = currentIndex === totalQuestions - 1;
  const hasCompleteAnswer = q => {
    const answer=answers[q.id] || '';
    if (!answer.trim()) return false;
    if ((q.question_type||'mcq')==='mcq') return (q.options||[]).some(o=>o.id===answer);
    if (q.question_type==='matching') {
      const entries=Object.fromEntries(answer.split('|').map(piece=>piece.split(':')).filter(parts=>parts.length===2));
      const selected=(q.meta?.left||[]).map(left=>entries[left]);
      return selected.length>=2 && selected.every(x=>x && (q.meta?.right||[]).includes(x)) && new Set(selected).size===selected.length;
    }
    if (q.question_type==='arrangement') return answer.split(' ').filter(Boolean).length === (q.meta?.tokens||[]).length;
    return true;
  };
  const allAnswered = questions.every(hasCompleteAnswer);

  const handleSelectOption = (optionId) => {
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: optionId
    }));
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    if (secondsLeft===0) {setError('Time has expired. Start a new attempt.');return;}
    if (!allAnswered) {
      setError('Please select an answer before submitting.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      const formattedAnswers = questions.map(q => ({
        question_id: q.id,
        ...(q.question_type && q.question_type !== 'mcq' ? { text: answers[q.id] } : { option_id: answers[q.id] })
      }));

      // Submit through API (secure scoring)
      const res = await api.submitQuiz(lessonId, user?.id, formattedAnswers, attemptToken);
      setResult(res);
      await refreshData();
    } catch (err) {
      console.error('Quiz submission failed:', err);
      setError(err.message || 'Failed to submit quiz results. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRetry = () => {
    setAnswers({});
    setCurrentIndex(0);
    setResult(null);
    setError(null);
    begin();
  };

  // If completed, show results view
  if (result) {
    return (
      <QuizResult
        result={result}
        onRetry={handleRetry}
        onNextLesson={onNextLesson}
        onBackToCourse={onBackToCourse}
      />
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {secondsLeft!==null&&<p role="timer" className="rounded-xl border bg-amber-50 px-4 py-3 text-sm font-bold text-amber-900">Time left: {Math.floor(secondsLeft/60)}:{String(secondsLeft%60).padStart(2,'0')}{secondsLeft===0&&<button type="button" className="ml-3 underline" onClick={handleRetry}>Restart attempt</button>}</p>}
      {!sessionReady&&<p className="text-sm text-slate-500">Opening secure quiz session…</p>}
      {/* Quiz Progress Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
          <span>
            Question {currentIndex + 1} of {totalQuestions}
          </span>
          <span>{Object.keys(answers).length} of {totalQuestions} answered</span>
        </div>
        <ProgressBar progress={progressPercent} size="sm" color="brand" />
      </div>

      <ErrorMessage message={error} />

      {/* Main Question Card */}
      <Card className="p-6 sm:p-8">
        <QuizQuestion
        languageCode={languageCode}
          question={currentQuestion}
          currentIndex={currentIndex}
          totalQuestions={totalQuestions}
          selectedOptionId={selectedOptionId}
          onSelectOption={handleSelectOption}
        />

        {/* Navigation / Action Bar */}
        <div className="pt-6 mt-8 border-t border-slate-100 flex items-center justify-between gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={handlePrevious}
            disabled={currentIndex === 0 || isSubmitting}
            icon={ArrowLeft}
          >
            Previous
          </Button>

          {isLastQuestion ? (
            <Button
              variant="success"
              size="md"
              onClick={handleSubmit}
              disabled={!allAnswered || secondsLeft===0 || !sessionReady || !attemptToken}
              isLoading={isSubmitting}
              icon={CheckCircle2}
            >
              Submit Quiz
            </Button>
          ) : (
            <Button
              variant="primary"
              size="md"
              onClick={handleNext}
              disabled={!hasCompleteAnswer(currentQuestion)}
              icon={ArrowRight}
            >
              Next Question
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
};
