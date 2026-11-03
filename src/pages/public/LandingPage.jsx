import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useLearning } from '../../contexts/LearningContext';
import { Button } from '../../components/common/Button';
import { Card } from '../../components/common/Card';
import { Badge } from '../../components/common/Badge';
import {
  Globe,
  BookOpen,
  CheckCircle2,
  Trophy,
  PlayCircle,
  ArrowRight,
  Shield,
  Sparkles,
  Zap,
  Users,
  Compass
} from 'lucide-react';

export const LandingPage = () => {
  const { isAuthenticated, quickDemoLogin, isSupabaseConnected } = useAuth();
  const { languages } = useLearning();
  const navigate = useNavigate();

  const handleStartLearning = (lang) => {
    if (isAuthenticated) {
      navigate(`/course/${lang.code || lang.id}`);
    } else {
      navigate('/register');
    }
  };

  const featureList = [
    {
      icon: Globe,
      title: 'Database-Driven Multi-Language',
      description: 'Learn ten languages through structured lessons, practice and progress tracking.'
    },
    {
      icon: PlayCircle,
      title: 'Integrated Video Lessons',
      description: 'Watch authentic educational YouTube video tutorials embedded directly within your study materials.'
    },
    {
      icon: Compass,
      title: 'Guided Vocabulary Practice',
      description: 'Build your vocabulary with real-world examples, translations and flashcards.'
    },
    {
      icon: Trophy,
      title: 'Automated Skill Assessments',
      description: 'Reinforce what you learn with multiple-choice quizzes and secure progress tracking.'
    },
    {
      icon: Zap,
      title: 'Structured CEFR Roadmaps',
      description: 'Progress naturally from A1 Beginner fundamentals to conversational confidence.'
    },
    {
      icon: Shield,
      title: 'Administrative Control Center',
      description: 'Manage languages, curricula, video links, vocabulary, and quizzes dynamically without code edits.'
    }
  ];

  const steps = [
    {
      step: '01',
      title: 'Select Your Target Language',
      description: 'Choose from ten supported languages and explore their CEFR learning paths.'
    },
    {
      step: '02',
      title: 'Study Curated Lessons & Videos',
      description: 'Master core grammar and practical vocabulary through interactive lessons.'
    },
    {
      step: '03',
      title: 'Pass Quizzes & Track Growth',
      description: 'Score 70%+ on interactive quizzes to unlock milestones and verify your mastery.'
    }
  ];

  return (
    <div className="space-y-24 py-8 sm:py-16">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-8">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 border border-brand-200/80 text-brand-700 text-xs font-semibold shadow-sm">
          <Sparkles className="w-4 h-4 text-brand-600" />
          <span>The Next-Generation Multi-Language EdTech Platform</span>
        </div>

        <div className="max-w-4xl mx-auto space-y-4">
          <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-[1.1]">
            Learn Languages.{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-600 to-indigo-600">
              Unlock Opportunities.
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Bridge global cultures with structured interactive lessons, vocabulary practice, and real-time progress assessment.
          </p>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          {isAuthenticated ? (
            <Link to="/dashboard">
              <Button size="lg" icon={ArrowRight}>
                Open Student Dashboard
              </Button>
            </Link>
          ) : (
            <>
              <Link to="/register">
                <Button size="lg" icon={Sparkles}>
                  Get Started Free
                </Button>
              </Link>
              <Link to="/languages">
                <Button variant="outline" size="lg" icon={BookOpen}>
                  Explore All Languages
                </Button>
              </Link>
            </>
          )}
        </div>

        {/* Offline demo only; production accounts never acquire roles via UI. */}
        {!isSupabaseConnected && <div className="pt-6 max-w-md mx-auto">
          <div className="p-3 bg-white rounded-2xl border border-slate-200/80 shadow-soft flex items-center justify-between gap-3 text-xs">
            <span className="text-slate-500 font-semibold pl-2">Instant Evaluation:</span>
            <div className="flex gap-2">
              <Button size="sm" variant="secondary" onClick={() => { quickDemoLogin('student'); navigate('/dashboard'); }}>
                Demo Student
              </Button>
              <Button size="sm" variant="secondary" onClick={() => { quickDemoLogin('admin'); navigate('/admin'); }} className="text-purple-700 bg-purple-50">
                Demo Admin
              </Button>
            </div>
          </div>
        </div>}
      </section>

      {/* Supported Languages Showcase */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-2">
          <Badge variant="primary" size="sm">Available Courses</Badge>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Start Learning Across 10 Languages
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            Every language includes structured A1 beginner lessons, vocabulary exercises, and interactive quizzes.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {languages.map((lang) => (
            <Card
              key={lang.id}
              hover
              onClick={() => handleStartLearning(lang)}
              className="p-5 text-center flex flex-col items-center justify-between group border-2 border-slate-100 hover:border-brand-200"
            >
              <div className="w-16 h-16 rounded-2xl bg-slate-50 flex items-center justify-center text-4xl mb-3 group-hover:scale-110 transition-transform shadow-sm">
                {lang.flag || '🌐'}
              </div>
              <h3 className="font-bold text-slate-900 group-hover:text-brand-600 transition-colors">
                {lang.name}
              </h3>
              <p className="text-xs font-semibold text-slate-400 mb-4 font-devanagari">
                {lang.native_name}
              </p>
              <Button size="sm" variant="outline" className="w-full text-xs">
                Start Course
              </Button>
            </Card>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-white border-y border-slate-200/80 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-14 space-y-2">
            <Badge variant="default" size="sm">Learning Methodology</Badge>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
              How LingoBridge Works
            </h2>
            <p className="text-xs sm:text-sm text-slate-500">
              A proven 3-step pedagogical loop designed for rapid retention and conversational fluency.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((item, idx) => (
              <div key={idx} className="relative p-6 rounded-2xl bg-slate-50/80 border border-slate-200/80 space-y-3">
                <span className="text-3xl font-black text-brand-600/30 block font-mono">
                  {item.step}
                </span>
                <h3 className="text-lg font-bold text-slate-900">{item.title}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Key Features Bento Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 space-y-2">
          <Badge variant="primary" size="sm">Key Features</Badge>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Engineered for Modern Language Learners
          </h2>
          <p className="text-xs sm:text-sm text-slate-500">
            A comprehensive full-stack architecture built with React, FastAPI, PostgreSQL, and intuitive UX.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {featureList.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <Card key={idx} className="p-6 space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center border border-brand-100">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-base font-bold text-slate-900">{feat.title}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{feat.description}</p>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl bg-gradient-to-tr from-slate-900 via-brand-950 to-brand-900 text-white p-8 sm:p-14 text-center space-y-6 relative overflow-hidden shadow-soft-lg">
          <div className="relative z-10 max-w-2xl mx-auto space-y-3">
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Begin Your Multi-Language Journey Today
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              Join other learners expanding their linguistic horizons. No credit card required.
            </p>
            <div className="pt-4 flex flex-wrap items-center justify-center gap-3">
              <Link to="/register">
                <Button size="lg" icon={Sparkles}>
                  Create Free Account
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
