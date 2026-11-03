import React from 'react';
import { CheckCircle2, Circle, ShieldCheck } from 'lucide-react';
import { checkPassword } from '../../utils/passwordPolicy';

export function PasswordStrength({ value }) {
  const result = checkPassword(value);
  const colors = ['bg-rose-500', 'bg-orange-500', 'bg-amber-500', 'bg-blue-500', 'bg-emerald-500'];
  return <section aria-label="Password strength" className="rounded-2xl border border-slate-200 bg-slate-50 p-4 space-y-3">
    <div className="flex items-center justify-between gap-2 text-xs">
      <span className="flex items-center gap-2 font-semibold text-slate-700"><ShieldCheck className="w-4 h-4"/>Password strength</span>
      <span aria-live="polite" className="font-bold text-slate-700">{result.level}</span>
    </div>
    <div role="progressbar" aria-label="Password rules satisfied" aria-valuemin={0} aria-valuemax={5} aria-valuenow={result.score} className="flex gap-1.5">
      {Array.from({ length: 5 }, (_, i) => <span key={i} className={`h-2 flex-1 rounded-full transition-colors duration-300 ${result.score > i ? colors[Math.max(0, result.score - 1)] : 'bg-slate-200'}`} />)}
    </div>
    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs">
      {result.checks.map(item => <li key={item.label} className={`flex gap-1.5 items-center ${item.passed ? 'text-emerald-700' : 'text-slate-500'}`}>
        {item.passed ? <CheckCircle2 className="w-3.5 h-3.5 shrink-0"/> : <Circle className="w-3.5 h-3.5 shrink-0"/>}{item.label}
      </li>)}
    </ul>
    {result.predictable && <p role="alert" className="text-xs text-rose-700">This password is too common. Choose a less predictable one.</p>}
  </section>;
}
