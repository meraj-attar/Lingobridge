import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { LearningProvider } from './contexts/LearningContext';

// Layouts
import { PublicLayout } from './components/layout/PublicLayout';
import { StudentLayout } from './components/layout/StudentLayout';
import { AdminLayout } from './components/layout/AdminLayout';

// Public & Auth Pages
import { LandingPage } from './pages/public/LandingPage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { ForgotPasswordPage } from './pages/auth/ForgotPasswordPage';
import { NotFoundPage } from './pages/public/NotFoundPage';

// Student Pages
import { StudentDashboard } from './pages/student/StudentDashboard';
import { LanguageSelectPage } from './pages/student/LanguageSelectPage';
import { CourseViewPage } from './pages/student/CourseViewPage';
import { LessonDetailPage } from './pages/student/LessonDetailPage';
import { QuizPage } from './pages/student/QuizPage';
import { ProfilePage } from './pages/student/ProfilePage';
import { FlashcardsPage } from './pages/student/FlashcardsPage';

// Admin Pages
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { ManageLanguagesPage } from './pages/admin/ManageLanguagesPage';
import { ManageLessonsPage } from './pages/admin/ManageLessonsPage';
import { ManageVocabularyPage } from './pages/admin/ManageVocabularyPage';
import { ManageQuizzesPage } from './pages/admin/ManageQuizzesPage';
import { ManageVideosPage } from './pages/admin/ManageVideosPage';
import { StudentOverviewPage } from './pages/admin/StudentOverviewPage';
import { CurriculumManagerPage } from './pages/admin/CurriculumManagerPage';

export function App() {
  return (
    <AuthProvider>
      <LearningProvider>
        <Routes>
          {/* Public Routes with Standard Navbar/Footer */}
          <Route element={<PublicLayout />}>
            <Route path="/" element={<LandingPage />} />
            <Route path="/languages" element={<LanguageSelectPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          </Route>

          {/* Protected Student Routes */}
          <Route element={<StudentLayout />}>
            <Route path="/dashboard" element={<StudentDashboard />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/flashcards" element={<FlashcardsPage />} />
            <Route path="/course/:code" element={<CourseViewPage />} />
            <Route path="/lesson/:id" element={<LessonDetailPage />} />
            <Route path="/lesson/:id/quiz" element={<QuizPage />} />
          </Route>

          {/* Protected Administrative Routes */}
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<AdminDashboard />} />
            <Route path="languages" element={<ManageLanguagesPage />} />
            <Route path="lessons" element={<ManageLessonsPage />} />
            <Route path="vocabulary" element={<ManageVocabularyPage />} />
            <Route path="quizzes" element={<ManageQuizzesPage />} />
            <Route path="videos" element={<ManageVideosPage />} />
            <Route path="students" element={<StudentOverviewPage />} />
            <Route path="curriculum" element={<CurriculumManagerPage />} />
          </Route>

          {/* Catch-all 404 Route */}
          <Route element={<PublicLayout />}>
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </LearningProvider>
    </AuthProvider>
  );
}

export default App;
