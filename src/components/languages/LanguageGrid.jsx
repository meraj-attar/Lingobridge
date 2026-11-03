import React from 'react';
import { LanguageCard } from './LanguageCard';

export const LanguageGrid = ({
  languages = [],
  enrolledMap = {},
  progressMap = {},
  lessonCountsMap = {},
  onSelectLanguage
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {languages.map((language) => (
        <LanguageCard
          key={language.id}
          language={language}
          isEnrolled={!!enrolledMap[language.id]}
          progress={progressMap[language.id] || 0}
          lessonCount={lessonCountsMap[language.id] || 5}
          onSelect={onSelectLanguage}
        />
      ))}
    </div>
  );
};
