export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

export const formatTimeAgo = (dateString) => {
  if (!dateString) return 'Never';
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);

  if (diffInSeconds < 60) return 'Just now';
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;
  return formatDate(dateString);
};

export const getLevelBadgeClass = (code = 'A1') => {
  switch (code.toUpperCase()) {
    case 'A1':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    case 'A2':
      return 'bg-teal-50 text-teal-700 border-teal-200';
    case 'B1':
      return 'bg-blue-50 text-brand-700 border-blue-200';
    case 'B2':
      return 'bg-indigo-50 text-indigo-700 border-indigo-200';
    case 'C1':
      return 'bg-purple-50 text-purple-700 border-purple-200';
    case 'C2':
      return 'bg-rose-50 text-rose-700 border-rose-200';
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200';
  }
};
