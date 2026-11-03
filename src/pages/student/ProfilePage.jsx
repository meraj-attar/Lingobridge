import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useAuth } from '../../contexts/AuthContext';
import { useLearning } from '../../contexts/LearningContext';
import { api } from '../../services/api';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { UserRound, BookMarked, Flame, Trophy, Clock } from 'lucide-react';

export function ProfilePage() {
  const {user, updateProfile} = useAuth();
  const {languages,progress} = useLearning();
  const [form,setForm]=useState({full_name:user?.full_name||'',native_language_id:user?.native_language_id||'',target_language_id:user?.target_language_id||'',daily_goal:user?.daily_goal||15});
  const [activity,setActivity]=useState(null);
  const [bookmarks,setBookmarks]=useState([]);
  const [message,setMessage]=useState('');
  const [error,setError]=useState('');
  useEffect(()=>{api.getActivity().then(setActivity).catch(e=>setError(e.message));api.getBookmarks().then(setBookmarks).catch(e=>setError(e.message));},[]);
  const save=async e=>{e.preventDefault();try {setError('');await updateProfile({...form,native_language_id:form.native_language_id||null,target_language_id:form.target_language_id||null,daily_goal:Number(form.daily_goal)});setMessage('Profile saved to your account.');}catch(e){setError(e.message);}};
  const courseLang=languages.find(l=>l.id===form.target_language_id);
  return <div className="max-w-5xl mx-auto space-y-6 pb-12">
    <div><h1 className="text-2xl font-black text-slate-900 flex gap-2 items-center"><UserRound/> My Profile & Learning History</h1><p className="text-sm text-slate-500">Your information and learning progress are stored on the server.</p></div>
    <div className="grid md:grid-cols-2 gap-6">
      <Card className="p-6"><h2 className="text-lg font-bold mb-4">Learning Preferences</h2><form onSubmit={save} className="space-y-4">
        <label className="block text-sm">Name<input value={form.full_name} required minLength={2} maxLength={160} onChange={e=>setForm({...form,full_name:e.target.value})} className="mt-1 w-full border rounded-xl p-3" /></label>
        <label className="block text-sm">Native / support language<select className="mt-1 w-full border rounded-xl p-3" value={form.native_language_id} onChange={e=>setForm({...form,native_language_id:e.target.value})}><option value="">Choose language</option>{languages.map(l=><option key={l.id} value={l.id}>{l.name} — {l.native_name}</option>)}</select></label>
        <label className="block text-sm">Target learning language<select className="mt-1 w-full border rounded-xl p-3" value={form.target_language_id} onChange={e=>setForm({...form,target_language_id:e.target.value})}><option value="">Choose language</option>{languages.map(l=><option key={l.id} value={l.id}>{l.name} — {l.native_name}</option>)}</select></label>
        <label className="block text-sm">Daily learning goal (minutes)<input type="number" min="1" max="240" className="mt-1 w-full border rounded-xl p-3" value={form.daily_goal} onChange={e=>setForm({...form,daily_goal:e.target.value})}/></label>
        {error&&<p className="text-red-600 text-sm" role="alert">{error}</p>}{message&&<p className="text-green-700 text-sm" role="status">{message}</p>}
        <Button type="submit">Save Preferences</Button>{courseLang&&<Link className="text-sm ml-3 text-brand-600" to={`/course/${courseLang.code}`}>Open selected course</Link>}
      </form></Card>
      <Card className="p-6 space-y-5"><h2 className="text-lg font-bold">Your Activity</h2><div className="grid grid-cols-3 gap-3 text-center"><div className="bg-brand-50 p-3 rounded-xl"><Trophy className="mx-auto text-brand-600"/><p className="font-black text-xl">{activity?.xp??0}</p><p className="text-xs">XP</p></div><div className="bg-orange-50 p-3 rounded-xl"><Flame className="mx-auto text-orange-600"/><p className="font-black text-xl">{activity?.streak??0}</p><p className="text-xs">Streak days</p></div><div className="bg-green-50 p-3 rounded-xl"><Clock className="mx-auto text-green-600"/><p className="font-black text-xl">{activity?.level??1}</p><p className="text-xs">Level</p></div></div>
        <div className="text-sm rounded-xl border bg-slate-50 p-3"><b>Today's learning goal:</b> {activity?.today_minutes||0} / {activity?.daily_goal||15} minutes · {activity?.daily_goal_percent||0}% {activity?.daily_goal_met?'✓ Goal reached':''}</div><h3 className="text-sm font-bold">Learning minutes credited by day</h3><div className="h-44"><ResponsiveContainer width="100%" height="100%"><BarChart data={[...(activity?.daily_activity||[])].reverse().slice(-14)}><XAxis dataKey="day" tick={{fontSize:10}}/><YAxis tick={{fontSize:10}}/><Tooltip/><Bar dataKey="minutes" fill="#2563eb" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div>
        <h3 className="text-sm font-bold">Achievements</h3>{activity?.achievements?.length ? <div className="flex gap-2 flex-wrap">{activity.achievements.map(a=><span key={a.code} className="bg-amber-50 border border-amber-200 text-amber-700 p-2 rounded-lg text-xs">🏅 {a.code.replaceAll('_',' ')}</span>)}</div>:<p className="text-sm text-slate-500">Complete your first quiz to unlock badges.</p>}
      </Card>
    </div>
    <div className="grid md:grid-cols-2 gap-6"><Card className="p-6"><h2 className="text-lg font-bold mb-3 flex items-center gap-2"><BookMarked/> Saved Lessons</h2>{bookmarks.length ? bookmarks.map(b=><div key={b.id} className="flex justify-between items-center py-2 border-b"><Link className="text-brand-600 text-sm" to={`/lesson/${b.lesson_id}`}>Open saved lesson</Link><button className="text-xs text-red-600" onClick={async()=>{await api.unbookmark(b.lesson_id);setBookmarks(items=>items.filter(x=>x.id!==b.id));}}>Remove</button></div>):<p className="text-sm text-slate-500">Bookmark lessons to find them here.</p>}<Link to="/flashcards" className="inline-block mt-4 text-sm text-brand-600">Practise flashcards →</Link></Card>
    <Card className="p-6"><h2 className="text-lg font-bold mb-3">Recent Quiz Attempts</h2>{progress.quiz_attempts.length?progress.quiz_attempts.slice(0,10).map(a=><div key={a.id} className="flex justify-between border-b py-2 text-sm"><Link className="text-brand-600" to={`/lesson/${a.lesson_id}`}>Lesson</Link><span>{a.percentage}% {a.passed?'✓':'·'} </span><span className="text-slate-500">{new Date(a.attempted_at).toLocaleDateString()}</span></div>):<p className="text-slate-500 text-sm">No quiz attempts yet.</p>}</Card></div>
  </div>;
}
