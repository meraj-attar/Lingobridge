import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { Sparkles, Compass } from 'lucide-react';

export const WelcomeBanner = () => {
  const { user } = useAuth();
  const firstName = user?.full_name?.split(' ')[0] || 'Learner';

  const motivationalQuotes = [
    "“To have another language is to possess a second soul.” – Charlemagne",
    "“One language sets you in a corridor for life. Two languages open every door along the way.” – Frank Smith",
    "“A different language is a different vision of life.” – Federico Fellini",
    "“The limits of my language mean the limits of my world.” – Ludwig Wittgenstein"
  ];

  const randomQuote = motivationalQuotes[0];

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-brand-700 via-brand-600 to-indigo-700 text-white p-6 sm:p-8 shadow-soft-lg">
      {/* Background Decorative Graphic */}
      <div className="absolute -right-12 -bottom-12 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none" />
      <div className="absolute right-12 top-6 opacity-10 pointer-events-none">
        <Compass className="w-48 h-48 text-white" />
      </div>

      <div className="relative z-10 max-w-2xl space-y-2">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 text-white text-xs font-semibold backdrop-blur-sm">
          <Sparkles className="w-3.5 h-3.5 text-amber-300" />
          <span>Keep your momentum going!</span>
        </div>

        <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
          Welcome back, {firstName}! 👋
        </h1>

        <p className="text-xs sm:text-sm text-brand-100 font-medium leading-relaxed italic pt-1">
          {randomQuote}
        </p>
      </div>
    </div>
  );
};
