import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLearning } from '../../contexts/LearningContext';
import { useAuth } from '../../contexts/AuthContext';
import { LanguageGrid } from '../../components/languages/LanguageGrid';
import { LoadingState } from '../../components/common/LoadingState';
import { Badge } from '../../components/common/Badge';
import { Card } from '../../components/common/Card';
import { Globe, Search, Sparkles } from 'lucide-react';

export const LanguageSelectPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const {
    languages,
    allLessons,
    enrolledLanguages,
    getLanguageProgress,
    enrollLanguage,
    isLoading
  } = useLearning();

  const [searchQuery, setSearchQuery] = useState('');

  if (isLoading) {
    return <LoadingState fullPage message="Loading active languages..." />;
  }

  // Build enrollment and progress maps
  const enrolledMap = {};
  enrolledLanguages.forEach(e => {
    enrolledMap[e.language_id] = true;
  });

  const progressMap = {};
  const lessonCountsMap = {};

  languages.forEach(lang => {
    progressMap[lang.id] = getLanguageProgress(lang.id);
    const langLessons = allLessons.filter(l => l.language_id === lang.id && l.is_published);
    lessonCountsMap[lang.id] = langLessons.length;
  });

  // Filter languages by active status and search
  const filteredLanguages = languages
    .filter(lang => lang.is_active)
    .filter(lang => {
      const q = searchQuery.toLowerCase();
      return (
        lang.name.toLowerCase().includes(q) ||
        lang.native_name.toLowerCase().includes(q) ||
        lang.code.toLowerCase().includes(q)
      );
    });

  const handleSelectLanguage = (language) => {
    navigate(isAuthenticated ? `/course/${language.code || language.id}` : '/register');
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <Badge variant="primary" size="md">
          <Globe className="w-3.5 h-3.5" />
          Course Catalogue
        </Badge>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">
          Choose a Language to Learn
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
          Learn multiple languages simultaneously with independent progress tracking, vocabulary practice and interactive quizzes.
        </p>
      </div>

      {/* Search Bar */}
      <div className="max-w-md mx-auto">
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            placeholder="Search language (e.g. Marathi, हिन्दी, English)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-900 shadow-sm transition-all placeholder:text-slate-400"
          />
        </div>
      </div>

      {/* Language Grid */}
      {filteredLanguages.length > 0 ? (
        <LanguageGrid
          languages={filteredLanguages}
          enrolledMap={enrolledMap}
          progressMap={progressMap}
          lessonCountsMap={lessonCountsMap}
          onSelectLanguage={handleSelectLanguage}
        />
      ) : (
        <Card className="text-center p-8 max-w-md mx-auto">
          <p className="text-sm font-semibold text-slate-700">No matching languages found</p>
          <p className="text-xs text-slate-500 mt-1">Try adjusting your search query.</p>
        </Card>
      )}
    </div>
  );
};
