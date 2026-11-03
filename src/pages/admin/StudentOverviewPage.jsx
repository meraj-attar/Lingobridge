import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { LoadingState } from '../../components/common/LoadingState';
import { formatDate } from '../../utils/formatters';
import { Users, Search, Trophy, CheckCircle2, BookOpen } from 'lucide-react';

export const StudentOverviewPage = () => {
  const [students, setStudents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('all');
  const [sort, setSort] = useState('recent');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [actionError,setActionError] = useState('');
  const [loadError,setLoadError] = useState('');

  useEffect(() => {
    let cancelled = false;
    const fetchStudents = async () => {
      try {
        setIsLoading(true);
        setLoadError('');
        const data = await api.getStudentsPage({page, page_size:10, search:searchQuery, status:filter, sort});
        if (!cancelled) {
          setStudents(data.items || []);
          setTotal(data.total || 0);
          setTotalPages(data.pages || 1);
        }
      } catch (err) {
        if (!cancelled) { setStudents([]); setTotal(0); setLoadError(err.message || 'Unable to load student records'); }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    // Delay searches to avoid sending one request per keystroke.
    const timer = setTimeout(fetchStudents, searchQuery ? 250 : 0);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [page, searchQuery, filter, sort]);

  const visibleStudents = students;

  const toggleActive=async student=>{if (!window.confirm(`${student.is_active ? 'Deactivate' : 'Activate'} account for ${student.full_name}?`))return;try{setActionError('');const updated=await api.updateStudent(student.id,{is_active:!student.is_active});setStudents(old=>old.map(s=>s.id===student.id?{...s,...updated}:s));}catch(e){setActionError(e.message)}};
  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 flex items-center gap-2">
            <Users className="w-6 h-6 text-purple-600" />
            Student Overview & Engagement
          </h1>
          <p className="text-xs text-slate-500">
            Monitor registered learner progress, enrollments, and quiz performance.
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            placeholder="Search students..."
            value={searchQuery}
            onChange={(e) => {setSearchQuery(e.target.value);setPage(1);}}
            className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-purple-500 bg-white"
          />
        </div>
      </div>

      {loadError&&<p role="alert" className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">{loadError}</p>}
      <div className="flex flex-wrap gap-3"><label className="text-xs text-slate-600">Account status<select value={filter} onChange={e=>{setFilter(e.target.value);setPage(1)}} className="ml-2 rounded-lg border bg-white p-2"><option value="all">All</option><option value="active">Active</option><option value="inactive">Inactive</option></select></label><label className="text-xs text-slate-600">Sort<select value={sort} onChange={e=>{setSort(e.target.value);setPage(1);}} className="ml-2 rounded-lg border bg-white p-2"><option value="recent">Most recent</option><option value="name">Name A–Z</option></select></label></div>
      {actionError&&<p className="text-sm text-red-600" role="alert">{actionError}</p>}
      {/* Table */}
      {isLoading ? (
        <LoadingState message="Loading student progress records..." />
      ) : (
        <Card className="p-0 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 text-slate-700 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">Student</th>
                  <th className="py-3.5 px-4">Role</th>
                  <th className="py-3.5 px-6">Enrolled Languages</th>
                  <th className="py-3.5 px-4 text-center">Courses</th>
                  <th className="py-3.5 px-4 text-center">Lessons Finished</th>
                  <th className="py-3.5 px-4 text-center">Quizzes Taken</th>
                  <th className="py-3.5 px-4 text-center">Average Score</th>
                  <th className="py-3.5 px-6 text-right">Joined Date</th><th className="py-3.5 px-6 text-right">Account</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {visibleStudents.map((student) => {
                  const completedCount = student.lesson_progress?.filter(p => p.status === 'completed').length || 0;
                  const quizCount = student.quiz_attempts?.length || 0;

                  return (
                    <tr key={student.id} className="hover:bg-slate-50/70 transition-colors">
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-xl bg-brand-100 text-brand-700 font-bold flex items-center justify-center text-xs">
                            {student.full_name?.charAt(0) || 'U'}
                          </div>
                          <div>
                            <p className="font-bold text-slate-900 text-sm">{student.full_name}</p>
                            <p className="text-xs text-slate-400">{student.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <Badge variant={student.role === 'admin' ? 'purple' : 'default'} size="sm">
                          {student.role}
                        </Badge>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex flex-wrap gap-1">
                          {student.student_languages && student.student_languages.length > 0 ? (
                            student.student_languages.map((enr, idx) => (
                              <Badge key={idx} variant="primary" size="sm">
                                <span>{enr.languages?.flag || '🌐'}</span>
                                <span>{enr.languages?.name || 'Lang'}</span>
                              </Badge>
                            ))
                          ) : (
                            <span className="text-slate-400 italic">No courses</span>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-4 text-center">{student.course_enrollments?.length||0}</td>
                      <td className="py-4 px-4 text-center font-bold text-emerald-700">
                        {completedCount}
                      </td>
                      <td className="py-4 px-4 text-center font-bold text-slate-800">
                        {quizCount}
                      </td>
                      <td className="py-4 px-4 text-center font-semibold">{quizCount?Math.round(student.quiz_attempts.reduce((total,q)=>total+(q.percentage||0),0)/quizCount)+'%':'—'}</td>
                      <td className="py-4 px-6 text-right text-slate-400">{formatDate(student.created_at)}</td>
                      <td className="py-4 px-6 text-right"><button className="px-3 py-1.5 rounded-lg border text-xs font-semibold text-brand-600" onClick={()=>toggleActive(student)}>{student.is_active?'Deactivate':'Activate'}</button></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      )}
      {total===0&&!isLoading&&!loadError&&<p className="text-sm text-slate-500">No matching students found.</p>}
      {(totalPages>1)&&<div className="flex items-center justify-between gap-3 text-sm"><p className="text-slate-500">Page {page} of {totalPages} · {total} accounts</p><div className="flex gap-2"><button className="border rounded-lg p-2 disabled:opacity-50" disabled={page<=1} onClick={()=>setPage(p=>Math.max(1,p-1))}>Previous</button><button className="border rounded-lg p-2 disabled:opacity-50" disabled={page>=totalPages} onClick={()=>setPage(p=>Math.min(totalPages,p+1))}>Next</button></div></div>}
    </div>
  );
};
