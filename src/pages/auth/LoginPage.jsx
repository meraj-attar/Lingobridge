import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { ErrorMessage } from '../../components/common/ErrorMessage';
import { Globe, Eye, EyeOff, Lock, Mail, ArrowRight, Shield, Sparkles } from 'lucide-react';

export const LoginPage = () => {
  const { login, quickDemoLogin, isSupabaseConnected } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError('Please fill in all required fields.');
      return;
    }

    try {
      setIsLoading(true);
      setError('');
      const session = await login(email, password);
      navigate(session.role === 'admin' && from === '/dashboard' ? '/admin' : from, { replace: true });
    } catch (err) {
      setError(err.message || 'Invalid email or password.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = (targetRole) => {
    quickDemoLogin(targetRole);
    navigate(targetRole === 'admin' ? '/admin' : '/dashboard', { replace: true });
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-brand-600 text-white flex items-center justify-center mx-auto shadow-md shadow-brand-500/20">
            <Globe className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">
            Sign in to LingoBridge
          </h2>
          <p className="text-xs text-slate-500">
            Resume your multi-language learning journey
          </p>
        </div>

        {/* Card */}
        <Card className="p-6 sm:p-8 space-y-5">
          <ErrorMessage message={error} />
          {location.state?.notice && <p className="rounded-xl p-3 text-xs text-emerald-700 bg-emerald-50">{location.state.notice}</p>}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Field */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-900 transition-all placeholder:text-slate-400"
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Password
                </label>
                <Link
                  to="/forgot-password"
                  className="text-xs font-semibold text-brand-600 hover:text-brand-700"
                >
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-900 transition-all placeholder:text-slate-400"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              variant="primary"
              size="md"
              className="w-full"
              isLoading={isLoading}
              icon={ArrowRight}
            >
              Sign In
            </Button>
          </form>

          {/* Demo access is available only in the explicitly offline local mode. */}
          {!isSupabaseConnected && <div className="pt-4 border-t border-slate-100 space-y-2">
            <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider text-center">
              Quick 1-Click Evaluation Logins
            </p>
            <div className="grid grid-cols-2 gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleDemoLogin('student')}
                className="text-xs"
                icon={Sparkles}
              >
                Student Demo
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleDemoLogin('admin')}
                className="text-xs text-purple-700 bg-purple-50 hover:bg-purple-100 border-purple-200"
                icon={Shield}
              >
                Admin Demo
              </Button>
            </div>
          </div>}
        </Card>

        {/* Footer Link */}
        <p className="text-center text-xs text-slate-500">
          Don't have an account yet?{' '}
          <Link to="/register" className="font-bold text-brand-600 hover:text-brand-700">
            Sign up for free
          </Link>
        </p>
      </div>
    </div>
  );
};
