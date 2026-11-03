import React from 'react';
import { Loader2 } from 'lucide-react';

export const Button = ({
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  className = '',
  disabled = false,
  isLoading = false,
  onClick,
  icon: Icon,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-offset-2 active:scale-[0.98] disabled:opacity-50 disabled:pointer-events-none disabled:active:scale-100';

  const variants = {
    primary: 'bg-brand-600 text-white hover:bg-brand-700 shadow-sm focus:ring-brand-500 border border-transparent',
    secondary: 'bg-slate-100 text-slate-800 hover:bg-slate-200 focus:ring-slate-400 border border-slate-200/80',
    outline: 'bg-white text-slate-700 hover:bg-slate-50 border border-slate-300 focus:ring-brand-500 shadow-sm',
    success: 'bg-emerald-600 text-white hover:bg-emerald-700 focus:ring-emerald-500 shadow-sm border border-transparent',
    danger: 'bg-rose-600 text-white hover:bg-rose-700 focus:ring-rose-500 shadow-sm border border-transparent',
    ghost: 'bg-transparent text-slate-600 hover:bg-slate-100 hover:text-slate-900 focus:ring-slate-300'
  };

  const sizes = {
    sm: 'text-xs px-3 py-1.5 gap-1.5 min-h-[32px]',
    md: 'text-sm px-4 py-2.5 gap-2 min-h-[42px]',
    lg: 'text-base px-6 py-3.5 gap-2.5 min-h-[50px] font-semibold'
  };

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      onClick={onClick}
      className={`${baseStyles} ${variants[variant] || variants.primary} ${sizes[size] || sizes.md} ${className}`}
      {...props}
    >
      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin shrink-0" />
      ) : Icon ? (
        <Icon className="w-4 h-4 shrink-0" />
      ) : null}
      <span>{children}</span>
    </button>
  );
};
