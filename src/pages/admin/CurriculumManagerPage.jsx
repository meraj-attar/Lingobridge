import React,{useEffect,useState} from 'react';
import {api} from '../../services/api';
import {Card} from '../../components/common/Card';
import {Button} from '../../components/common/Button';

const config={
 levels:{code:'text',name:'text',description:'textarea',sort_order:'number'},
 courses:{language_id:'language',level_id:'level',title:'text',description:'textarea',is_published:'boolean'},
 modules:{course_id:'course',title:'text',sort_order:'number'},
 achievements:{code:'text',title:'text',description:'textarea',threshold:'number'}
};
export function CurriculumManagerPage(){
 const [table,setTable]=useState('courses');const [rows,setRows]=useState([]);const [languages,setLanguages]=useState([]);const [levels,setLevels]=useState([]);const [courses,setCourses]=useState([]);const [form,setForm]=useState({});const [editId,setEditId]=useState(null);const [error,setError]=useState('');const [status,setStatus]=useState('');const [loading,setLoading]=useState(false);
 const load=async()=>{setLoading(true);try{const [items,ls,lv,cs]=await Promise.all([api.adminList(table),api.getLanguages(),api.getLevels(),api.getCourses()]);setRows(items);setLanguages(ls);setLevels(lv);setCourses(cs);setError('');}catch(e){setError(e.message)}finally{setLoading(false)}};
 useEffect(()=>{setEditId(null);setForm({});load();},[table]);
 const fields=config[table];
 const save=async e=>{e.preventDefault();try{setError('');if(editId)await api.adminUpdate(table,editId,form);else await api.adminCreate(table,form);setStatus(editId?'Updated successfully':'Created successfully');setEditId(null);setForm({});await load();}catch(err){setError(err.message)}};
 const remove=async id=>{if(!window.confirm('Delete this item? Existing linked data may prevent deletion.'))return;try{await api.adminDelete(table,id);await load();setStatus('Deleted');}catch(e){setError(e.message)}};
 return <div className="space-y-6"><h1 className="text-2xl font-black">Course, Module & Proficiency Management</h1><p className="text-sm text-slate-500">All edits persist in PostgreSQL. Existing relationships are protected by constraints.</p><div className="flex flex-wrap gap-2">{Object.keys(config).map(t=><button key={t} onClick={()=>setTable(t)} className={`px-4 py-2 rounded-xl text-sm ${table===t?'bg-purple-600 text-white':'bg-white border'}`}>{t[0].toUpperCase()+t.slice(1)}</button>)}</div>
 {error&&<p role="alert" className="text-red-700 p-3 bg-red-50 rounded-xl">{error}</p>}{status&&<p role="status" className="text-green-700">{status}</p>}
 <Card className="p-5"><h2 className="font-bold mb-4">{editId?'Edit':'Add'} {table.slice(0,-1)}</h2><form onSubmit={save} className="grid sm:grid-cols-2 gap-4">{Object.entries(fields).filter(([key])=>!(editId&&key==='code'&&table==='achievements')).map(([field,type])=><label key={field} className="text-xs font-semibold text-slate-600">{field.replaceAll('_',' ')}
 {type==='boolean'?<input type="checkbox" className="ml-2" checked={form[field]??true} onChange={e=>setForm({...form,[field]:e.target.checked})}/>:['language','level','course'].includes(type)?<select required value={form[field]||''} onChange={e=>setForm({...form,[field]:e.target.value})} className="w-full mt-1 p-3 border rounded-xl"><option value="">Select</option>{(type==='language'?languages:type==='level'?levels:courses).map(v=><option key={v.id} value={v.id}>{v.title||v.name||v.code}</option>)}</select>:type==='textarea'?<textarea rows="2" className="w-full mt-1 p-3 border rounded-xl" value={form[field]||''} onChange={e=>setForm({...form,[field]:e.target.value})}/>:<input required type={type} className="w-full mt-1 p-3 border rounded-xl" value={form[field]??''} onChange={e=>setForm({...form,[field]:type==='number'?Number(e.target.value):e.target.value})}/>}</label>)}<div className="col-span-full flex gap-3"><Button type="submit">{editId?'Save Changes':'Create Item'}</Button>{editId&&<Button variant="outline" onClick={()=>{setEditId(null);setForm({})}} type="button">Cancel</Button>}</div></form></Card>
 <Card className="p-4"><h2 className="font-bold mb-3">Existing {table} ({rows.length})</h2>{loading?<p>Loading records…</p>:<div className="space-y-2">{rows.map(r=><div key={r.id||r.code} className="flex flex-wrap items-center justify-between gap-3 border-b p-3 text-sm"><div><p className="font-semibold">{r.title||r.name||r.code}</p><p className="text-xs text-slate-500">{r.description||r.id}</p></div><div className="flex gap-2"><button className="text-brand-600" onClick={()=>{setEditId(r.id||r.code);setForm(Object.fromEntries(Object.keys(fields).filter(k=>k in r).map(k=>[k,r[k]])));window.scrollTo({top:0,behavior:'smooth'})}}>Edit</button><button className="text-red-600" onClick={()=>remove(r.id||r.code)}>Delete</button></div></div>)}</div>}</Card>
 </div>;
}
