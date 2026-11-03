import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../../components/common/Button';
import { Globe, Home, ArrowLeft } from 'lucide-react';

export const NotFoundPage = () => {
  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <div className="text-center space-y-4 max-w-md">
        <div className="w-16 h-16 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto border border-brand-100">
          <Globe className="w-8 h-8" />
        </div>
        <h1 className="text-4xl font-black text-slate-900 tracking-tight">404</h1>
        <h2 className="text-lg font-bold text-slate-800">Page Not Found</h2>
        <p className="text-xs text-slate-500 leading-relaxed">
          The learning resource or page you are looking for might have been moved or does not exist.
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <Link to="/">
            <Button variant="primary" size="sm" icon={Home}>
              Return Home
            </Button>
          </Link>
          <Link to="/languages">
            <Button variant="outline" size="sm">
              Browse Courses
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};
