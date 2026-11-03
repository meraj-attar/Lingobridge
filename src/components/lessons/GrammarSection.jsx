import React from 'react';
import { BookOpen, Lightbulb } from 'lucide-react';

// Minimal safe Markdown formatting for seeded lesson explanations. No HTML
// interpretation or dangerouslySetInnerHTML: user-authored Markdown is text.
const inlineText = value => String(value).split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g).map((part,index) => {
  if (part.startsWith('**') && part.endsWith('**')) return <strong key={index}>{part.slice(2,-2)}</strong>;
  if (part.startsWith('*') && part.endsWith('*')) return <em key={index}>{part.slice(1,-1)}</em>;
  return <React.Fragment key={index}>{part}</React.Fragment>;
});

const lessonBlocks = text => {
  const blocks=[];
  const lines=String(text||'').split(/\r?\n/);
  let paragraph=[];
  let list=[];
  const flushParagraph=()=>{
    if (paragraph.length) {
      blocks.push({type:'paragraph',text:paragraph.join(' ')});
      paragraph=[];
    }
  };
  const flushList=()=>{
    if (list.length) { blocks.push({type:'list',items:list});list=[]; }
  };
  lines.forEach(line => {
    const trimmed=line.trim();
    if (!trimmed) { flushParagraph();flushList();return; }
    const heading=trimmed.match(/^(#{2,4})\s+(.+)$/);
    if (heading) {
      flushParagraph();flushList();
      blocks.push({type:'heading',level:heading[1].length,text:heading[2]});
    } else if (trimmed.startsWith('- ')) {
      flushParagraph();list.push(trimmed.slice(2));
    } else {
      flushList();paragraph.push(trimmed);
    }
  });
  flushParagraph();flushList();
  return blocks;
};

export const GrammarSection = ({ grammarNotes, content }) => (
  <div className="space-y-6">
    {grammarNotes && <div className="bg-amber-50/70 border border-amber-200/80 rounded-2xl p-5 flex items-start gap-4">
      <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center shrink-0">
        <Lightbulb className="w-5 h-5" />
      </div>
      <div><h4 className="text-sm font-bold text-amber-900 mb-1">Grammar &amp; Structure Note</h4>
        <p className="text-xs text-amber-800 leading-relaxed">{inlineText(grammarNotes)}</p></div>
    </div>}
    <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-soft">
      <div className="flex items-center gap-2 mb-6 pb-4 border-b border-slate-100">
        <BookOpen className="w-5 h-5 text-brand-600" />
        <h3 className="text-base font-bold text-slate-900">Lesson Explanation &amp; Rules</h3>
      </div>
      <div className="prose prose-slate max-w-none text-sm text-slate-700 leading-relaxed space-y-4">
        {content ? lessonBlocks(content).map((block,index) => {
          if (block.type==='heading') return block.level===2
            ? <h2 key={index} className="text-xl font-bold text-slate-900 mt-4">{inlineText(block.text)}</h2>
            : block.level===3 ? <h3 key={index} className="text-lg font-bold text-slate-900 mt-3">{inlineText(block.text)}</h3>
              : <h4 key={index} className="text-base font-bold text-slate-800 mt-2">{inlineText(block.text)}</h4>;
          if (block.type==='list') return <ul key={index} className="list-disc ps-5 space-y-1">{block.items.map((item,i) => <li key={i}>{inlineText(item)}</li>)}</ul>;
          return <p key={index}>{inlineText(block.text)}</p>;
        }) : <p className="text-xs text-slate-400 italic">No text explanation added yet.</p>}
      </div>
    </div>
  </div>
);
