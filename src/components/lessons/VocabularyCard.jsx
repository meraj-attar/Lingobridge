import React from 'react';

export const VocabularyCard = ({ item, languageCode = 'en' }) => {
  const rtl = String(languageCode).toLowerCase().startsWith('ur');
  return (
    <div lang={languageCode} dir={rtl ? 'rtl' : 'ltr'} className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-soft hover:shadow-soft-lg transition-all duration-200 flex flex-col justify-between group">
      <div>
        <div className="flex items-start justify-between gap-3 mb-2">
          <div>
            <h4 className="text-xl font-bold text-slate-900 tracking-tight group-hover:text-brand-600 transition-colors">{item.word}</h4>
            {item.pronunciation && <span className="text-xs font-mono text-slate-400">{item.pronunciation}</span>}
          </div>
        </div>
        <p className="text-sm font-semibold text-slate-700 mb-3 pb-3 border-b border-slate-100" lang="en" dir="ltr">{item.translation}</p>
        {item.example_sentence && <div className="bg-slate-50/80 rounded-xl p-3 border border-slate-100 space-y-1">
          <p className="text-sm font-medium text-slate-800">{item.example_sentence}</p>
          {item.example_translation && <p className="text-xs text-slate-500 italic" lang="en" dir="ltr">{item.example_translation}</p>}
        </div>}
      </div>
    </div>
  );
};
