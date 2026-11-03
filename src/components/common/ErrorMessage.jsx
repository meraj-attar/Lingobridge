import React from 'react';
import { AlertCircle } from 'lucide-react';

export const ErrorMessage = ({ message, className = '' }) => {
  if (!message) return null;

  return (
    <div className={`p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 flex items-start gap-3 ${className}`}>
      <AlertCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
      <div className="text-sm font-medium">{message}</div>
    </div>
  );
};
