import React from 'react';
import { Check, RotateCcw } from 'lucide-react';

export const QuizQuestion = ({ question, currentIndex, totalQuestions, selectedOptionId, onSelectOption, languageCode = 'en' }) => {
  const type = question.question_type || 'mcq';
  const details = question.meta || {};
  const match = Object.fromEntries((selectedOptionId || '').split('|').map(item => item.split(':')).filter(a => a.length===2));
  const chosen = (selectedOptionId || '').split(' ').filter(Boolean);
  return <div className="space-y-6" lang={languageCode} dir={String(languageCode).startsWith('ur') ? 'rtl' : 'ltr'}>
    <div>
      <span className="text-xs font-bold uppercase text-brand-600">Question {currentIndex+1} of {totalQuestions}</span>
      <span className="text-xs text-slate-400 ml-3">{({mcq:'Multiple Choice',fill_blank:'Fill in the Blank',matching:'Matching',arrangement:'Sentence Arrangement'})[type] || type}</span>
      <h3 className="mt-2 text-lg sm:text-xl font-bold text-slate-900 font-devanagari">{question.question_text}</h3>
    </div>
    {type==='mcq' && <div className="space-y-3">{(question.options || []).map((opt,index) => <div key={opt.id} className={`flex items-center gap-2 border-2 rounded-2xl p-2 ${selectedOptionId===opt.id ? 'border-brand-600 bg-brand-50' : 'border-slate-200 bg-white'}`}>
      <button type="button" aria-pressed={selectedOptionId===opt.id} onClick={() => onSelectOption(opt.id)} className="flex-1 flex items-center gap-3 text-start p-2 min-w-0">
        <span className="rounded-xl bg-slate-100 py-1.5 px-3 font-bold">{String.fromCharCode(65+index)}</span>
        <span className="flex-1 font-devanagari">{opt.option_text}</span>
        {selectedOptionId===opt.id && <Check className="w-4 h-4 text-brand-600" />}
      </button>
    </div>)}</div>}
    {type==='fill_blank' && <div className="space-y-4"><p className="text-base font-bold text-slate-800 font-devanagari">{details.prompt}</p><label className="text-xs font-semibold text-slate-500">Enter the missing word</label><input aria-label="Missing word" className="w-full p-3 border border-slate-300 rounded-xl font-devanagari" value={selectedOptionId || ''} onChange={e => onSelectOption(e.target.value)} placeholder="Type the missing word" /></div>}
    {type==='matching' && <div className="space-y-3"><p className="text-xs text-slate-500">Select the correct phrase for each item.</p>{(details.left || []).map(left => <div key={left} className="grid grid-cols-[90px_1fr] items-center gap-3"><strong className="text-slate-800">{left}</strong><select aria-label={`Match ${left}`} value={match[left]||''} className="p-3 border rounded-xl font-devanagari min-w-0" onChange={e=>onSelectOption((details.left||[]).map(x => `${x}:${x===left?e.target.value:match[x]||''}`).join('|'))}><option value="">Choose match</option>{(details.right||[]).map(right=><option key={right} value={right}>{right}</option>)}</select></div>)}</div>}
    {type==='arrangement' && <div className="space-y-3"><p className="text-xs text-slate-500">Tap the words in the correct order.</p><div className="min-h-14 border-2 border-dashed rounded-xl p-3 font-devanagari">{selectedOptionId || 'Your sentence appears here...'}</div><div className="flex flex-wrap gap-2">{[...(details.tokens||[])].map((word,i)=><button type="button" key={i} disabled={chosen.filter(x=>x===word).length >= (details.tokens||[]).slice(0,i+1).filter(x=>x===word).length && chosen.includes(word)} onClick={()=>onSelectOption([...chosen,word].join(' '))} className="border bg-white rounded-lg px-3 py-2 hover:bg-brand-50 font-devanagari">{word}</button>)}</div><button type="button" className="text-xs text-brand-600 flex gap-1 items-center" onClick={()=>onSelectOption('')}><RotateCcw size={14}/> Clear order</button></div>}
  </div>;
};
