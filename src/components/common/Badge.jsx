import React from 'react';

export const Badge = ({
  children,
  variant = 'default',
  size = 'md',
  className = ''
}) => {
  const variants = {
    default: 'bg-slate-100 text-slate-700 border-slate-200',
    primary: 'bg-brand-50 text-brand-700 border-brand-200',
    success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    danger: 'bg-rose-50 text-rose-700 border-rose-200',
    purple: 'bg-purple-50 text-purple-700 border-purple-200'
  };

  const sizes = {
    sm: 'text-[11px] font-medium px-2 py-0.5 rounded-md',
    md: 'text-xs font-semibold px-2.5 py-1 rounded-lg',
    lg: 'text-sm font-semibold px-3 py-1.5 rounded-xl'
  };

  return (
    <span
      className={`inline-flex items-center gap-1 border ${variants[variant] || variants.default} ${
        sizes[size] || sizes.md
      } ${className}`}
    >
      {children}
    </span>
  );
};
