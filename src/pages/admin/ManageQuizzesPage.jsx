import React,{useEffect,useState} from 'react';
import {api} from '../../services/api';
import {useLearning} from '../../contexts/LearningContext';
import {Card} from '../../components/common/Card';
import {Button} from '../../components/common/Button';
import {Modal} from '../../components/common/Modal';
import {HelpCircle,Plus,Pencil,Trash2} from 'lucide-react';

const TYPES=[['mcq','Multiple choice'],['fill_blank','Fill in the blank'],['matching','Matching'],['arrangement','Sentence arrangement']];
const blank=()=>({question_text:'',explanation:'',question_type:'mcq',time_limit_seconds:'',answer_text:'',prompt:'',pairs:'',tokens:'',options:[{option_text:'',is_correct:true},{option_text:'',is_correct:false},{option_text:'',is_correct:false},{option_text:'',is_correct:false}]});
const toForm=q=>({
 question_text:q.question_text,explanation:q.explanation||'',question_type:q.question_type||'mcq',
 time_limit_seconds:q.time_limit_seconds||'',answer_text:q.answer_text||'',prompt:q.meta?.prompt||'',
 pairs:(q.meta?.pairs||[]).map(p=>p.join(' = ')).join('\n'),tokens:(q.meta?.tokens||[]).join(' | '),
 options:q.options?.length?q.options.map(o=>({option_text:o.option_text,is_correct:o.is_correct})):blank().options
});
function payload(f){
 const base={question_text:f.question_text.trim(),explanation:f.explanation.trim(),question_type:f.question_type,time_limit_seconds:f.time_limit_seconds?Number(f.time_limit_seconds):null};
 if(f.question_type==='mcq')return {...base,answer_text:null,meta:{},options:f.options};
 if(f.question_type==='fill_blank')return {...base,answer_text:f.answer_text.trim(),meta:{prompt:f.prompt.trim()}};
 if(f.question_type==='matching')return {...base,answer_text:null,meta:{pairs:f.pairs.split('\n').filter(x=>x.trim()).map(line=>line.split(' = ').map(s=>s.trim()))}};
 return {...base,answer_text:f.answer_text.trim(),meta:{tokens:f.tokens.split('|').map(x=>x.trim()).filter(Boolean)}};
}
export const ManageQuizzesPage=()=>{
 const {languages}=useLearning();const [lessons,setLessons]=useState([]),[languageId,setLanguageId]=useState(''),[lessonId,setLessonId]=useState(''),[questions,setQuestions]=useState([]);
 const [busy,setBusy]=useState(false),[error,setError]=useState(''),[status,setStatus]=useState(''),[show,setShow]=useState(false),[form,setForm]=useState(blank),[editId,setEditId]=useState(null);
 useEffect(()=>{api.adminList('lessons').then(setLessons).catch(e=>setError(e.message));},[]);
 useEffect(()=>{if(languages.length&&!languageId)setLanguageId(languages[0].id);},[languages,languageId]);
 const filtered=lessons.filter(l=>l.language_id===languageId);
 useEffect(()=>{if(!filtered.some(l=>l.id===lessonId))setLessonId(filtered[0]?.id||'');},[languageId,lessons]);
 const reload=async()=>{if(!lessonId){setQuestions([]);return;}setBusy(true);try{const data=await api.getLessonById(lessonId,{includeAnswers:true});setQuestions(data.quiz_questions||[]);setError('');}catch(e){setError(e.message)}finally{setBusy(false)}};
 useEffect(()=>{reload();},[lessonId]);
 const open=q=>{setEditId(q?.id||null);setForm(q?toForm(q):blank());setError('');setShow(true)};
 const save=async e=>{e.preventDefault();setError('');let data=payload(form);
   if(!data.question_text){setError('Enter the question text.');return;}
   if(data.question_type==='mcq'&&(data.options.length<2||data.options.length>8||data.options.filter(o=>o.is_correct).length!==1||data.options.some(o=>!o.option_text.trim()))){setError('Add 2–8 options and select one correct answer.');return;}
   if(data.question_type==='matching'&&(data.meta.pairs.length<2||data.meta.pairs.some(p=>p.length!==2||!p[0]||!p[1]))){setError('Enter at least two pairs, one per line, using left = right.');return;}
   if(data.question_type==='arrangement'&&data.meta.tokens.join(' ')!==data.answer_text){setError('Answer must match the ordered words, separated by |.');return;}
   if(data.question_type==='fill_blank'&&(!data.answer_text||!data.meta.prompt.includes('_____'))){setError('Provide the missing word and a prompt containing _____.');return;}
   setBusy(true);try{if(editId)await api.editQuizQuestion(editId,data);else await api.addQuizQuestion(lessonId,data);setStatus(editId?'Question updated':'Question created');setShow(false);await reload();}
   catch(e){setError(e.message)}finally{setBusy(false)}
 };
 const remove=async q=>{if(!window.confirm('Delete this question permanently?'))return;try{await api.deleteQuizQuestion(lessonId,q.id);setStatus('Question deleted');await reload()}catch(e){setError(e.message)}};
 return <div className="space-y-6 pb-12">
  <div className="flex flex-wrap items-center justify-between gap-4"><div><h1 className="text-2xl font-black flex items-center gap-2"><HelpCircle className="text-purple-600"/> Manage Exercises & Quizzes</h1><p className="text-sm text-slate-500">Create, edit and delete MCQ, fill-in, matching and arrangement questions. Answer keys stay on the server.</p></div><Button icon={Plus} disabled={!lessonId} onClick={()=>open(null)}>Add Question</Button></div>
  {error&&<p role="alert" className="bg-red-50 text-red-700 border rounded-xl p-3 text-sm">{error}</p>}{status&&<p role="status" className="text-green-700 text-sm">{status}</p>}
  <Card className="p-4 grid sm:grid-cols-2 gap-4"><label className="text-xs font-semibold">Language<select className="mt-2 border rounded-xl p-3 w-full" value={languageId} onChange={e=>setLanguageId(e.target.value)}>{languages.map(l=><option key={l.id} value={l.id}>{l.name}</option>)}</select></label><label className="text-xs font-semibold">Lesson<select className="mt-2 border rounded-xl p-3 w-full" value={lessonId} onChange={e=>setLessonId(e.target.value)}>{filtered.map(l=><option key={l.id} value={l.id}>{l.title}</option>)}</select></label></Card>
  {busy&&!show&&<p>Loading questions…</p>}{!busy&&!questions.length&&<Card className="p-6 text-slate-500">No questions for this lesson yet.</Card>}
  <div className="space-y-3">{questions.map((q,i)=><Card key={q.id} className="p-5"><div className="flex items-start justify-between gap-3"><div><p className="text-xs text-brand-600 font-semibold">Question {i+1} · {TYPES.find(x=>x[0]===q.question_type)?.[1]||'Multiple choice'}</p><h3 className="font-bold font-devanagari mt-1">{q.question_text}</h3><p className="text-xs text-slate-500 mt-2">{q.explanation}</p></div><div className="flex gap-3"><button className="text-brand-600 text-xs" onClick={()=>open(q)} aria-label="Edit question"><Pencil size={16}/></button><button className="text-rose-600" onClick={()=>remove(q)} aria-label="Delete question"><Trash2 size={16}/></button></div></div><div className="mt-3 grid sm:grid-cols-2 gap-2">{q.options?.map(o=><p key={o.id} className={`p-2 rounded-lg border text-xs font-devanagari ${o.is_correct?'bg-green-50 border-green-300':'bg-slate-50'}`}>{o.option_text}{o.is_correct?' ✓':''}</p>)}</div>{q.question_type!=='mcq'&&<p className="text-xs text-slate-600 mt-2">Answer: {q.question_type==='matching'?JSON.stringify(q.meta?.pairs):q.answer_text}</p>}</Card>)}</div>
  <Modal isOpen={show} onClose={()=>setShow(false)} title={editId?'Edit Question':'Add Question'} maxWidth="max-w-2xl"><form onSubmit={save} className="space-y-4 max-h-[75vh] overflow-y-auto p-1">
   {error&&<p className="text-red-600 text-sm" role="alert">{error}</p>}
   <label className="block text-xs font-bold">Exercise type<select className="block w-full border p-3 mt-1 rounded-xl" value={form.question_type} onChange={e=>setForm({...form,question_type:e.target.value})}>{TYPES.map(([v,label])=><option key={v} value={v}>{label}</option>)}</select></label>
   <label className="block text-xs font-bold">Question<textarea required rows="2" className="block w-full border p-3 mt-1 rounded-xl" value={form.question_text} onChange={e=>setForm({...form,question_text:e.target.value})}/></label>
   {form.question_type==='mcq'&&form.options.map((o,i)=><div key={i} className="flex gap-2 items-center"><input type="radio" name="correct" aria-label={`Mark option ${i+1} correct`} checked={o.is_correct} onChange={()=>setForm({...form,options:form.options.map((x,j)=>({...x,is_correct:i===j}))})}/><input aria-label={`Option ${i+1}`} placeholder={`Option ${i+1}`} required className="p-2 border rounded-xl flex-1 min-w-0" value={o.option_text} onChange={e=>setForm({...form,options:form.options.map((x,j)=>j===i?{...x,option_text:e.target.value}:x)})}/></div>)}
   {form.question_type==='mcq'&&<div className="flex flex-wrap gap-2 items-center">
    <Button type="button" variant="outline" disabled={form.options.length>=8 || busy} onClick={()=>setForm({...form,options:[...form.options,{option_text:'',is_correct:false}]})}>Add option ({form.options.length}/8)</Button>
    {form.options.length>2 && <Button type="button" variant="outline" disabled={busy || form.options[form.options.length-1].is_correct} onClick={()=>setForm({...form,options:form.options.slice(0,-1)})}>Remove last incorrect option</Button>}
    <span className="text-xs text-slate-500">2–8 options; select exactly one correct answer. To remove a correct option, choose a different correct answer first.</span>
   </div>}
   {form.question_type==='fill_blank'&&<><label className="block text-xs font-bold">Prompt with _____ for missing word<input required className="block w-full p-3 border rounded-xl mt-1" value={form.prompt} onChange={e=>setForm({...form,prompt:e.target.value})}/></label><label className="block text-xs font-bold">Correct missing word<input required className="block w-full p-3 border rounded-xl mt-1" value={form.answer_text} onChange={e=>setForm({...form,answer_text:e.target.value})}/></label></>}
   {form.question_type==='matching'&&<label className="block text-xs font-bold">Matching pairs (one per line: left = right)<textarea required rows="5" className="block w-full p-3 border rounded-xl mt-1" value={form.pairs} onChange={e=>setForm({...form,pairs:e.target.value})}/></label>}
   {form.question_type==='arrangement'&&<><label className="block text-xs font-bold">Ordered tokens separated with |<textarea required rows="2" className="block w-full p-3 border rounded-xl mt-1" value={form.tokens} onChange={e=>setForm({...form,tokens:e.target.value,answer_text:e.target.value.split('|').map(x=>x.trim()).join(' ')})}/></label><p className="text-xs text-slate-600">Resulting answer: {form.answer_text}</p></>}
   <label className="block text-xs font-bold">Explanation<textarea className="block w-full p-3 border rounded-xl mt-1" rows="2" value={form.explanation} onChange={e=>setForm({...form,explanation:e.target.value})}/></label>
   <label className="block text-xs font-bold">Optional timer (seconds, 10–3600)<input className="block w-full p-3 border rounded-xl mt-1" type="number" min="10" max="3600" value={form.time_limit_seconds} onChange={e=>setForm({...form,time_limit_seconds:e.target.value})}/></label>
   <div className="flex gap-3 justify-end"><Button type="button" variant="outline" onClick={()=>setShow(false)}>Cancel</Button><Button type="submit" disabled={busy}>{busy?'Saving…':'Save Question'}</Button></div>
  </form></Modal>
 </div>;
};
