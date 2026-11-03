import React,{useEffect,useState} from 'react';
import {Link} from 'react-router-dom';
import {api} from '../../services/api';
import {useLearning} from '../../contexts/LearningContext';
import {Card} from '../../components/common/Card';
import {Button} from '../../components/common/Button';

export function FlashcardsPage(){
 const {allLessons,languages,enrolledCourses}=useLearning();
 const [selected,setSelected]=useState(''),[cards,setCards]=useState([]),[states,setStates]=useState({}),[index,setIndex]=useState(0),[revealed,setRevealed]=useState(false),[error,setError]=useState(''),[saving,setSaving]=useState(false),[filter,setFilter]=useState('all');
 const enrolledIds=new Set(enrolledCourses.map(x=>x.language_id));
 const target=selected||enrolledCourses[0]?.language_id||'';
 useEffect(()=>{let live=true;const eligible=allLessons.filter(l=>l.language_id===target&&l.is_published&&enrolledCourses.some(c=>c.id===l.course_id));
 setCards([]);setIndex(0);setRevealed(false);setError('');
 Promise.all([Promise.all(eligible.map(l=>api.getLessonById(l.id))),api.getFlashcardStates()]).then(([data,saved])=>{if(!live)return;setCards(data.flatMap(l=>l.vocabulary_items||[]));setStates(Object.fromEntries(saved.map(s=>[s.vocabulary_id,s])))}).catch(e=>{if(live)setError(e.message)});
 return ()=>{live=false};},[target,allLessons,enrolledCourses]);
 const due = card => !states[card.id] || states[card.id].due;
 const visible=cards.filter(card=>filter==='all'||(filter==='due'?due(card):(states[card.id]?.state||'revise')===filter));
 const card=visible[Math.min(index,Math.max(visible.length-1,0))];const language=languages.find(l=>l.id===target);
 const choose=async state=>{if(!card)return;setSaving(true);setError('');try{const saved=await api.setFlashcardState(card.id,state);setStates(s=>({...s,[card.id]:saved}));setRevealed(false);setIndex(i=>Math.min(i,Math.max(0,visible.length-2)));}catch(e){setError(e.message)}finally{setSaving(false)}};
 return <div className="max-w-2xl mx-auto space-y-6"><Link className="text-brand-600 text-sm" to="/dashboard">← Dashboard</Link><h1 className="text-2xl font-black">Vocabulary Flashcards</h1><p className="text-slate-500 text-sm">Reviews are scheduled on your account. “Due” includes new and missed cards; known words return at increasing intervals.</p>
 <div className="grid sm:grid-cols-2 gap-3"><label className="text-sm">Learning language<select className="block mt-1 w-full p-3 border rounded-xl" value={target} onChange={e=>setSelected(e.target.value)}>{languages.filter(l=>enrolledIds.has(l.id)).map(l=><option key={l.id} value={l.id}>{l.name}</option>)}</select></label>
 <label className="text-sm">Review list<select value={filter} onChange={e=>{setFilter(e.target.value);setIndex(0)}} className="block mt-1 w-full p-3 border rounded-xl"><option value="all">All words ({cards.length})</option><option value="due">Due to review ({cards.filter(due).length})</option><option value="revise">Revise ({cards.filter(c=>(states[c.id]?.state||'revise')==='revise').length})</option><option value="known">Known ({cards.filter(c=>states[c.id]?.state==='known').length})</option></select></label></div>
 {error&&<p role="alert" className="text-red-600">{error}</p>}{card?<><Card className="p-8 text-center min-h-56 flex flex-col justify-center items-center gap-3"><p className="text-xs text-slate-500">Card {Math.min(index+1,visible.length)} of {visible.length} · {states[card.id]?.state==='known'?'Known':'Revise'}</p><h2 lang={language?.code||'en'} dir={language?.code==='ur'?'rtl':'ltr'} className="text-2xl font-bold font-devanagari">{card.word}</h2>{revealed&&<><p className="text-base">{card.translation}</p><p lang={language?.code||'en'} dir={language?.code==='ur'?'rtl':'ltr'} className="font-devanagari text-sm text-slate-500">{card.example_sentence}</p></>}<Button onClick={()=>setRevealed(x=>!x)}>{revealed?'Hide Answer':'Reveal Answer'}</Button></Card>
 <div className="flex flex-wrap justify-between gap-2"><Button variant="outline" disabled={index===0} onClick={()=>{setIndex(i=>i-1);setRevealed(false)}}>Previous</Button><Button disabled={saving} onClick={()=>choose('revise')}>Review Tomorrow</Button><Button disabled={saving} onClick={()=>choose('known')}>Remembered</Button><Button variant="outline" disabled={index>=visible.length-1} onClick={()=>{setIndex(i=>i+1);setRevealed(false)}}>Next</Button></div></>:<Card className="p-8 text-center text-slate-500">{target?'No words match your current review selection.':'Enroll in a course to begin.'}</Card>}</div>;
}
