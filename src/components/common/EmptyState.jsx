import React from 'react';
import { Button } from './Button';
import { Inbox } from 'lucide-react';

export const EmptyState = ({
  icon: Icon = Inbox,
  title = 'No items found',
  description = 'There are no records to display at this moment.',
  actionLabel,
  onAction
}) => {
  return (
    <div className="text-center py-12 px-4 rounded-2xl border-2 border-dashed border-slate-200 bg-white/50 max-w-lg mx-auto">
      <div className="w-14 h-14 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto mb-4 border border-slate-200/80">
        <Icon className="w-7 h-7" />
      </div>
      <h3 className="text-base font-semibold text-slate-900 mb-1">{title}</h3>
      <p className="text-xs text-slate-500 max-w-sm mx-auto mb-6">{description}</p>
      {actionLabel && onAction && (
        <Button onClick={onAction} size="sm">
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
