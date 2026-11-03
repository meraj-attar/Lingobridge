import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from './Button';
import {
  Globe,
  BookOpen,
  LayoutDashboard,
  Shield,
  LogOut,
  User,
  Menu,
  X,
  Sparkles,
  ChevronDown
} from 'lucide-react';

export const Navbar = () => {
  const { user, role, isAdmin, isAuthenticated, logout, quickDemoLogin, isSupabaseConnected } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const isCurrent = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 to-brand-500 text-white flex items-center justify-center shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
              <Globe className="w-5 h-5" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-extrabold tracking-tight text-slate-900 leading-none">
                Lingo<span className="text-brand-600">Bridge</span>
              </span>
              <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mt-0.5">
                Multi-Language Learning
              </span>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-1">
            <Link
              to="/languages"
              className={`px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
                isCurrent('/languages')
                  ? 'bg-brand-50 text-brand-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Browse Languages
            </Link>
            
            {isAuthenticated && (
              <Link
                to="/dashboard"
                className={`px-3 py-2 rounded-xl text-sm font-medium transition-colors ${
                  isCurrent('/dashboard')
                    ? 'bg-brand-50 text-brand-700 font-semibold'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                My Dashboard
              </Link>
            )}

            {isAdmin && (
              <Link
                to="/admin"
                className={`px-3 py-2 rounded-xl text-sm font-medium flex items-center gap-1.5 transition-colors ${
                  location.pathname.startsWith('/admin')
                    ? 'bg-purple-50 text-purple-700 font-semibold'
                    : 'text-purple-600 hover:text-purple-800 hover:bg-purple-50/60'
                }`}
              >
                <Shield className="w-4 h-4" />
                Admin Panel
              </Link>
            )}
          </nav>

          {/* Right Action Area */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                  className="flex items-center gap-2.5 p-1.5 pl-3 rounded-xl border border-slate-200 hover:border-slate-300 bg-white transition-all shadow-sm"
                >
                  <div className="w-8 h-8 rounded-lg bg-brand-100 text-brand-700 font-bold flex items-center justify-center text-xs">
                    {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <div className="text-left text-xs pr-1">
                    <p className="font-semibold text-slate-800 leading-none">{user?.full_name || 'Learner'}</p>
                    <span className={`inline-block text-[10px] font-bold uppercase tracking-wider mt-0.5 ${isAdmin ? 'text-purple-600' : 'text-brand-600'}`}>
                      {role}
                    </span>
                  </div>
                  <ChevronDown className="w-4 h-4 text-slate-400" />
                </button>

                {/* Dropdown Menu */}
                {userDropdownOpen && (
                  <div
                    className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-soft-lg border border-slate-200 py-2 z-50 animate-in fade-in zoom-in-95"
                    onClick={() => setUserDropdownOpen(false)}
                  >
                    <div className="px-4 py-2 border-b border-slate-100">
                      <p className="text-xs font-semibold text-slate-900 truncate">{user?.full_name}</p>
                      <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
                    </div>

                    <Link
                      to="/dashboard"
                      className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"
                    >
                      <LayoutDashboard className="w-4 h-4 text-slate-400" />
                      Student Dashboard
                    </Link>

                    <Link
                      to="/profile" className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"><User className="w-4 h-4"/> Profile &amp; Progress</Link>
                    <Link to="/flashcards" className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"><BookOpen className="w-4 h-4"/> Flashcards</Link>
                    <Link
                      to="/languages"
                      className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50"
                    >
                      <BookOpen className="w-4 h-4 text-slate-400" />
                      All Courses & Lessons
                    </Link>

                    {isAdmin && (
                      <Link
                        to="/admin"
                        className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-purple-700 hover:bg-purple-50"
                      >
                        <Shield className="w-4 h-4 text-purple-500" />
                        Admin Management
                      </Link>
                    )}

                    {/* Offline demo role switcher */}
                    {!isSupabaseConnected && <div className="px-3 py-2 border-t border-slate-100 mt-1">
                      <p className="text-[10px] uppercase font-bold text-slate-400 px-1 mb-1">Quick Role Switch</p>
                      <div className="grid grid-cols-2 gap-1.5">
                        <button
                          type="button"
                          onClick={() => quickDemoLogin('student')}
                          className={`text-[11px] font-semibold py-1 px-2 rounded-lg border text-center transition-colors ${
                            role === 'student'
                              ? 'bg-brand-50 border-brand-300 text-brand-700'
                              : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                          }`}
                        >
                          Student
                        </button>
                        <button
                          type="button"
                          onClick={() => quickDemoLogin('admin')}
                          className={`text-[11px] font-semibold py-1 px-2 rounded-lg border text-center transition-colors ${
                            role === 'admin'
                              ? 'bg-purple-50 border-purple-300 text-purple-700'
                              : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                          }`}
                        >
                          Admin
                        </button>
                      </div>
                    </div>}

                    <div className="border-t border-slate-100 pt-1">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-4 py-2 text-xs font-medium text-rose-600 hover:bg-rose-50 text-left"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                {/* 1-Click Demo Buttons (offline only) */}
                {!isSupabaseConnected && <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => quickDemoLogin('student')}
                  className="text-xs"
                >
                  Student Demo
                </Button>}
                {!isSupabaseConnected && <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => quickDemoLogin('admin')}
                  className="text-xs text-purple-700 border-purple-200 bg-purple-50 hover:bg-purple-100"
                >
                  Admin Demo
                </Button>}
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    Log In
                  </Button>
                </Link>
                <Link to="/register">
                  <Button variant="primary" size="sm">
                    Get Started Free
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Toggle */}
          <div className="flex items-center md:hidden gap-2">
            {isAuthenticated && (
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${isAdmin ? 'bg-purple-50 text-purple-700 border-purple-200' : 'bg-brand-50 text-brand-700 border-brand-200'}`}>
                {role}
              </span>
            )}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-6 space-y-3">
          <Link
            to="/languages"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50"
          >
            Browse Languages
          </Link>
          {isAuthenticated && (
            <>
              <Link
                to="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Student Dashboard
              </Link>
              {isAdmin && (
                <Link
                  to="/admin"
                  onClick={() => setMobileMenuOpen(false)}
                  className="block px-3 py-2 rounded-lg text-sm font-bold text-purple-700 bg-purple-50"
                >
                  Admin Panel
                </Link>
              )}
            </>
          )}

          <div className="pt-3 border-t border-slate-100 flex flex-col gap-2">
            {isAuthenticated ? (
              <>
                <div className="flex items-center justify-between px-2 text-xs text-slate-600">
                  <span>Signed in as <b>{user?.full_name}</b></span>
                  <span className="uppercase text-[10px] font-bold text-brand-600">({role})</span>
                </div>
                {!isSupabaseConnected && <div className="grid grid-cols-2 gap-2 my-1">
                  <Button size="sm" variant="secondary" onClick={() => quickDemoLogin('student')}>
                    Switch to Student
                  </Button>
                  <Button size="sm" variant="secondary" onClick={() => quickDemoLogin('admin')}>
                    Switch to Admin
                  </Button>
                </div>}
                <Button variant="danger" size="sm" onClick={handleLogout} className="w-full">
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Link to="/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="outline" size="sm" className="w-full">
                    Log In
                  </Button>
                </Link>
                <Link to="/register" onClick={() => setMobileMenuOpen(false)}>
                  <Button variant="primary" size="sm" className="w-full">
                    Get Started Free
                  </Button>
                </Link>
                {!isSupabaseConnected && <div className="grid grid-cols-2 gap-2 pt-1">
                  <Button size="sm" variant="secondary" onClick={() => { quickDemoLogin('student'); setMobileMenuOpen(false); }}>
                    Demo Student
                  </Button>
                  <Button size="sm" variant="secondary" onClick={() => { quickDemoLogin('admin'); setMobileMenuOpen(false); }}>
                    Demo Admin
                  </Button>
                </div>}
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};
