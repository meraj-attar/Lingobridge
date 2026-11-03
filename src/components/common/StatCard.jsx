import React from 'react';
import { Card } from './Card';

export const StatCard = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  color = 'blue'
}) => {
  const colorMaps = {
    blue: 'bg-blue-50 text-brand-600 border-blue-100',
    green: 'bg-emerald-50 text-emerald-600 border-emerald-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
    amber: 'bg-amber-50 text-amber-600 border-amber-100',
    rose: 'bg-rose-50 text-rose-600 border-rose-100'
  };

  return (
    <Card className="flex items-center gap-4">
      {Icon && (
        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center border shrink-0 ${colorMaps[color] || colorMaps.blue}`}>
          <Icon className="w-6 h-6" />
        </div>
      )}
      <div className="flex-1 min-w-0">
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider truncate">{title}</p>
        <div className="flex items-baseline gap-2 mt-1">
          <p className="text-2xl font-bold text-slate-900 tracking-tight">{value}</p>
          {trend && <span className="text-xs font-semibold text-emerald-600">{trend}</span>}
        </div>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5 truncate">{subtitle}</p>}
      </div>
    </Card>
  );
};
