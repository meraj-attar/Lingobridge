import React from 'react';
import { VocabularyCard } from './VocabularyCard';
import { Sparkles } from 'lucide-react';

export const VocabularyList = ({ items = [], languageCode = 'en' }) => {
  if (!items || items.length === 0) {
    return (
      <div className="p-8 text-center bg-slate-50 rounded-2xl border border-slate-200">
        <p className="text-xs text-slate-500">No vocabulary items registered for this lesson yet.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-brand-600" />
          Lesson Vocabulary ({items.length} words)
        </h3>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item) => (
          <VocabularyCard key={item.id || item.word} item={item} languageCode={languageCode} />
        ))}
      </div>
    </div>
  );
};
