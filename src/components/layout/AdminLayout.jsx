import React, { useState } from 'react';
import { Outlet, Navigate, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { LoadingState } from '../common/LoadingState';
import {
  LayoutDashboard,
  Languages,
  BookOpen,
  SpellCheck,
  HelpCircle,
  Video,
  Users,
  Shield,
  ArrowLeft,
  Menu,
  X,
  Sparkles
} from 'lucide-react';

export const AdminLayout = () => {
  const { isAdmin, isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  if (isLoading) {
    return <LoadingState fullPage message="Verifying administrative credentials..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl border border-slate-200 text-center shadow-soft">
          <div className="w-14 h-14 bg-rose-100 text-rose-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Shield className="w-7 h-7" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">Access Restricted</h2>
          <p className="text-xs text-slate-500 mb-6 leading-relaxed">
            Administrator privileges are required to access this console. Please sign in with an authorized administrator account.
          </p>
          <div className="flex flex-col gap-2">
            <Link
              to="/dashboard"
              className="inline-flex items-center justify-center px-4 py-2.5 rounded-xl bg-brand-600 text-white text-sm font-semibold hover:bg-brand-700"
            >
              Return to Student Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const navItems = [
    { label: 'Overview', path: '/admin', icon: LayoutDashboard },
    { label: 'Manage Languages', path: '/admin/languages', icon: Languages },
    { label: 'Courses & Modules', path: '/admin/curriculum', icon: BookOpen },
    { label: 'Manage Lessons', path: '/admin/lessons', icon: BookOpen },
    { label: 'Manage Vocabulary', path: '/admin/vocabulary', icon: SpellCheck },
    { label: 'Manage Quizzes', path: '/admin/quizzes', icon: HelpCircle },
    { label: 'Video Lessons', path: '/admin/videos', icon: Video },
    { label: 'Student Overview', path: '/admin/students', icon: Users }
  ];

  const isNavActive = (path) => {
    if (path === '/admin') {
      return location.pathname === '/admin';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen flex bg-slate-100/70">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-64 bg-slate-900 text-white shrink-0 border-r border-slate-800">
        {/* Brand */}
        <div className="p-6 border-b border-slate-800">
          <Link to="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-purple-600 text-white flex items-center justify-center">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h2 className="font-extrabold text-sm tracking-tight text-white leading-none">
                Lingo<span className="text-purple-400">Admin</span>
              </h2>
              <p className="text-[10px] text-slate-400 font-semibold uppercase tracking-wider mt-0.5">
                Content Management
              </p>
            </div>
          </Link>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isNavActive(item.path);
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  active
                    ? 'bg-purple-600 text-white shadow-md shadow-purple-900/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/80'
                }`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Return to Student View footer */}
        <div className="p-4 border-t border-slate-800 space-y-3">
          <div className="px-3 py-2 bg-slate-800/60 rounded-xl">
            <p className="text-[11px] font-bold text-white truncate">{user?.full_name}</p>
            <span className="inline-block text-[9px] font-bold text-purple-400 uppercase">
              Super Admin Mode
            </span>
          </div>

          <Link
            to="/dashboard"
            className="flex items-center justify-center gap-2 w-full py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            Student View
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Admin Header (Mobile & Sticky Top) */}
        <header className="sticky top-0 z-30 bg-white border-b border-slate-200/80 px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileSidebarOpen(!mobileSidebarOpen)}
              className="lg:hidden p-2 rounded-xl text-slate-600 hover:bg-slate-100"
            >
              {mobileSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <h1 className="text-base font-bold text-slate-800">Administrator Console</h1>
          </div>

          <div className="flex items-center gap-3">
            <Link
              to="/dashboard"
              className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Exit Admin
            </Link>
          </div>
        </header>

        {/* Mobile Sidebar overlay */}
        {mobileSidebarOpen && (
          <div className="lg:hidden bg-slate-900 text-white p-4 space-y-2 border-b border-slate-800">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isNavActive(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileSidebarOpen(false)}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-semibold ${
                    active ? 'bg-purple-600 text-white' : 'text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        )}

        {/* Admin View Body */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
