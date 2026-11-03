import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingState = ({ message = 'Loading content...', fullPage = false }) => {
  if (fullPage) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-9 h-9 text-brand-600 animate-spin" />
        <p className="text-sm font-medium text-slate-600">{message}</p>
      </div>
    );
  }

  return (
    <div className="py-12 flex flex-col items-center justify-center gap-2">
      <Loader2 className="w-6 h-6 text-brand-600 animate-spin" />
      <p className="text-xs text-slate-500 font-medium">{message}</p>
    </div>
  );
};
