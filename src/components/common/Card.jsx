import React from 'react';

export const Card = ({
  children,
  className = '',
  hover = false,
  onClick,
  ...props
}) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl border border-slate-200/80 p-6 shadow-soft ${
        hover ? 'transition-all duration-200 hover:shadow-soft-lg hover:-translate-y-0.5 cursor-pointer' : ''
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};
