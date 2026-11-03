import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Card } from '../../components/common/Card';
import { StatCard } from '../../components/common/StatCard';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { LoadingState } from '../../components/common/LoadingState';
import { Link } from 'react-router-dom';
import {
  Users,
  Languages,
  BookOpen,
  HelpCircle,
  Trophy,
  TrendingUp,
  Plus,
  ArrowRight,
  Shield,
  Clock,
  Sparkles
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [students, setStudents] = useState([]);
  const [languagesList, setLanguagesList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshIndex, setRefreshIndex] = useState(0);

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        setIsLoading(true); setError('');
        const [statsData, studentsData, langsData] = await Promise.all([
          api.getAdminStats(),
          api.getAllStudents(),
          api.getLanguages()
        ]);
        setStats(statsData);
        setStudents(studentsData);
        setLanguagesList(langsData);
      } catch (err) {
        setError(err.message || 'Could not load live platform statistics.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAdminData();
  }, [refreshIndex]);

  if (isLoading) {
    return <LoadingState fullPage message="Aggregating platform analytics..." />;
  }

  if (error && !stats) return <div role="alert" className="max-w-xl mx-auto rounded-2xl border border-rose-200 bg-rose-50 p-8 text-rose-800"><h1 className="font-bold text-xl">Analytics unavailable</h1><p className="text-sm my-3">{error}</p><button className="rounded-xl bg-rose-700 text-white px-4 py-2 text-sm" onClick={()=>setRefreshIndex(x=>x+1)}>Retry loading</button></div>;

  // Chart data for languages
  const languageChartData = languagesList.map(lang => ({
    name: lang.name,
    code: lang.code,
    flag: lang.flag
  }));

  const COLORS = ['#2563EB', '#EA580C', '#4F46E5', '#DC2626', '#CA8A04', '#10B981'];

  return (
    <div className="space-y-8 pb-12">
      {error && <div role="alert" className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-800">{error} <button className="underline font-semibold ml-2" onClick={()=>setRefreshIndex(x=>x+1)}>Retry</button></div>}
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-soft">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="purple" size="sm">
              <Shield className="w-3.5 h-3.5" />
              Administrator Control Center
            </Badge>
          </div>
          <h1 className="text-2xl font-black text-slate-900">Platform Analytics Overview</h1>
          <p className="text-xs text-slate-500">
            Real-time multi-language curriculum statistics and student engagement metrics.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button onClick={()=>setRefreshIndex(x=>x+1)} className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-xs font-semibold hover:bg-slate-50">Refresh data</button>
          <Link to="/admin/languages">
            <Button size="sm" variant="primary" icon={Plus}>
              New Language
            </Button>
          </Link>
          <Link to="/admin/lessons">
            <Button size="sm" variant="outline" icon={BookOpen}>
              Create Lesson
            </Button>
          </Link>
        </div>
      </div>

      {/* 1. Core KPIs Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard
          title="Registered Students"
          value={stats?.total_students ?? students.filter(s => s.role === 'student').length}
          subtitle="Total accounts"
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Active Languages"
          value={stats?.total_languages ?? languagesList.filter(l => l.is_active).length}
          subtitle="Supported courses"
          icon={Languages}
          color="purple"
        />
        <StatCard
          title="Published Lessons"
          value={stats?.total_lessons ?? 0}
          subtitle="Across all levels"
          icon={BookOpen}
          color="green"
        />
        <StatCard
          title="Active Quizzes"
          value={stats?.total_quizzes ?? 0}
          subtitle="Evaluations"
          icon={HelpCircle}
          color="amber"
        />
        <StatCard
          title="Quiz Attempts"
          value={stats?.total_attempts ?? 0}
          subtitle="Learner submissions"
          icon={Trophy}
          color="rose"
        />
        <StatCard
          title="Quiz Pass Rate"
          value={`${stats?.pass_rate ?? 0}%`}
          subtitle="Benchmark >= 70%"
          icon={TrendingUp}
          color="green"
        />
      </div>

      <div className="grid sm:grid-cols-2 gap-4"><Card className="p-5"><p className="text-xs font-semibold text-slate-500 uppercase">Total courses</p><p className="text-3xl font-black text-slate-900">{stats?.total_courses ?? '—'}</p></Card><Card className="p-5"><p className="text-xs font-semibold text-slate-500 uppercase">Vocabulary items</p><p className="text-3xl font-black text-slate-900">{stats?.total_vocabulary ?? '—'}</p></Card></div>

      {/* 2. Quick Action Management Shortcuts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 flex items-center justify-between group hover:border-purple-300">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900">Manage Languages</h3>
            <p className="text-xs text-slate-500">Manage active languages and locale settings</p>
          </div>
          <Link to="/admin/languages">
            <Button size="sm" variant="secondary" icon={ArrowRight}>
              Open
            </Button>
          </Link>
        </Card>

        <Card className="p-5 flex items-center justify-between group hover:border-purple-300">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900">Manage Lessons</h3>
            <p className="text-xs text-slate-500">Create, edit, or publish lessons</p>
          </div>
          <Link to="/admin/lessons">
            <Button size="sm" variant="secondary" icon={ArrowRight}>
              Open
            </Button>
          </Link>
        </Card>

        <Card className="p-5 flex items-center justify-between group hover:border-purple-300">
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-900">Quiz Questions</h3>
            <p className="text-xs text-slate-500">Configure 4-choice questions</p>
          </div>
          <Link to="/admin/quizzes">
            <Button size="sm" variant="secondary" icon={ArrowRight}>
              Open
            </Button>
          </Link>
        </Card>
      </div>

      {/* 3. Recent Registered Students Table Preview */}
      <Card className="p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">Recently Registered Students</h3>
            <p className="text-xs text-slate-500">Overview of registered learners and their active courses</p>
          </div>
          <Link to="/admin/students">
            <Button size="sm" variant="outline" icon={ArrowRight}>
              View All Students
            </Button>
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-slate-700 font-bold uppercase tracking-wider text-[10px]">
              <tr>
                <th className="py-3 px-4 rounded-l-xl">Student</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">Role</th>
                <th className="py-3 px-4">Enrolled Languages</th>
                <th className="py-3 px-4 rounded-r-xl">Completed Lessons</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {students.slice(0, 5).map((stu) => (
                <tr key={stu.id} className="hover:bg-slate-50/80">
                  <td className="py-3 px-4 font-bold text-slate-900 flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-brand-100 text-brand-700 font-bold flex items-center justify-center text-xs">
                      {stu.full_name?.charAt(0) || 'U'}
                    </div>
                    {stu.full_name}
                  </td>
                  <td className="py-3 px-4 text-slate-500">{stu.email}</td>
                  <td className="py-3 px-4">
                    <Badge variant={stu.role === 'admin' ? 'purple' : 'default'} size="sm">
                      {stu.role}
                    </Badge>
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-1">
                      {stu.student_languages && stu.student_languages.length > 0 ? (
                        stu.student_languages.map((enr, i) => (
                          <span key={i} title={enr.languages?.name} className="text-sm">
                            {enr.languages?.flag || '🌐'}
                          </span>
                        ))
                      ) : (
                        <span className="text-slate-400 italic">None</span>
                      )}
                    </div>
                  </td>
                  <td className="py-3 px-4 font-semibold text-slate-700">
                    {stu.lesson_progress?.filter(p => p.status === 'completed').length || 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
