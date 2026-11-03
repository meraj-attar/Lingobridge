import React from 'react';
import { Link } from 'react-router-dom';
import { Globe, Heart, Shield, BookOpen, Sparkles } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-white border-t border-slate-200/80 pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-1 space-y-3">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center">
                <Globe className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-slate-900">
                Lingo<span className="text-brand-600">Bridge</span>
              </span>
            </Link>
            <p className="text-xs text-slate-500 leading-relaxed">
              Empowering learners worldwide through interactive lessons, real-world dialogues, and structured quizzes.
            </p>
          </div>

          {/* Languages */}
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
              Supported Languages
            </h4>
            <ul className="space-y-2 text-xs text-slate-600 font-medium">
              <li><Link to="/languages" className="hover:text-brand-600 transition-colors">English (🇬🇧)</Link></li>
              <li><Link to="/languages" className="hover:text-brand-600 transition-colors">Hindi - हिन्दी (🇮🇳)</Link></li>
              <li><Link to="/languages" className="hover:text-brand-600 transition-colors">Marathi - मराठी (🇮🇳)</Link></li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
              Platform
            </h4>
            <ul className="space-y-2 text-xs text-slate-600 font-medium">
              <li><Link to="/" className="hover:text-brand-600 transition-colors">Home</Link></li>
              <li><Link to="/languages" className="hover:text-brand-600 transition-colors">Course Catalogue</Link></li>
              <li><Link to="/dashboard" className="hover:text-brand-600 transition-colors">Student Dashboard</Link></li>
              <li><Link to="/admin" className="hover:text-brand-600 transition-colors">Admin Portal</Link></li>
            </ul>
          </div>

          {/* Platform Highlights */}
          <div className="bg-slate-50 rounded-2xl p-4 border border-slate-200/80">
            <div className="flex items-center gap-2 text-xs font-bold text-brand-700 mb-1">
              <Sparkles className="w-4 h-4 text-brand-600" />
              <span>Free & Open EdTech</span>
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Zero paywalls or subscriptions. Built with modern full-stack architecture, FastAPI with PostgreSQL, and reactive UI.
            </p>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400">
          <p>© {new Date().getFullYear()} LingoBridge. Built for global language accessibility.</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1">
              Made with <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" /> for passionate learners
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
