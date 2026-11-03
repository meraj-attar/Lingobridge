import React from 'react';
import { StatCard } from '../common/StatCard';
import { useLearning } from '../../contexts/LearningContext';
import { Languages, CheckCircle2, Trophy, BarChart3 } from 'lucide-react';

export const QuickStats = () => {
  const {
    enrolledLanguages,
    enrolledCourses,
    getTotalCompletedLessons,
    getOverallQuizAverage,
    progress
  } = useLearning();

  const totalQuizzes = progress.quiz_attempts?.length || 0;
  const completedLessons = getTotalCompletedLessons();
  const avgScore = getOverallQuizAverage();
  const enrolledCount = enrolledCourses?.length || 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title="Enrolled Courses"
        value={enrolledCount}
        subtitle="Enrolled courses"
        icon={Languages}
        color="blue"
      />
      <StatCard
        title="Lessons Completed"
        value={completedLessons}
        subtitle="Verified progress"
        icon={CheckCircle2}
        color="green"
      />
      <StatCard
        title="Quizzes Taken"
        value={totalQuizzes}
        subtitle="Skill assessments"
        icon={Trophy}
        color="amber"
      />
      <StatCard
        title="Average Score"
        value={`${avgScore}%`}
        subtitle="Quiz accuracy"
        icon={BarChart3}
        color="purple"
      />
    </div>
  );
};
