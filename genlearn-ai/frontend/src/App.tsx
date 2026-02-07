import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { LanguageProvider } from './contexts/LanguageContext';

// Pages
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { LearningPage } from './pages/LearningPage';
import { AvatarPage } from './pages/AvatarPage';
import { CharactersPage } from './pages/CharactersPage';
import { TournamentsPage } from './pages/TournamentsPage';
import { LeaderboardPage } from './pages/LeaderboardPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';
import { HistoryPage } from './pages/HistoryPage';
import { RevisionPage } from './pages/RevisionPage';

// Enhanced Features Pages
import { LearnFromAnythingPage } from './pages/LearnFromAnythingPage';
import { ReverseClassroomPage } from './pages/ReverseClassroomPage';
import { TimeTravelPage } from './pages/TimeTravelPage';
import { ConceptCollisionPage } from './pages/ConceptCollisionPage';
import { MistakeAutopsyPage } from './pages/MistakeAutopsyPage';
import { YouTubeCoursePage } from './pages/YouTubeCoursePage';
import { DebateArenaPage } from './pages/DebateArenaPage';
import { DreamProjectPage } from './pages/DreamProjectPage';
import { FeynmanEnginePage } from './pages/FeynmanEnginePage';

// Admin Pages
import { AdminHomePage } from './pages/admin/AdminHomePage';
import { ManageTournamentsPage } from './pages/admin/ManageTournamentsPage';
import { ManageTeamsPage } from './pages/admin/ManageTeamsPage';
import { ManageQuestionsPage } from './pages/admin/ManageQuestionsPage';
import { ManageUsersPage } from './pages/admin/ManageUsersPage';


function App() {
  const { loadUser, isLoading } = useAuth();

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading..." />
      </div>
    );
  }

  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <DashboardPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/learning"
            element={
              <ProtectedRoute>
                <Layout>
                  <LearningPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/avatar"
            element={
              <ProtectedRoute>
                <Layout>
                  <AvatarPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/characters"
            element={
              <ProtectedRoute>
                <Layout>
                  <CharactersPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/tournaments"
            element={
              <ProtectedRoute>
                <Layout>
                  <TournamentsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/leaderboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <LeaderboardPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Layout>
                  <ProfilePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <Layout>
                  <SettingsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <Layout>
                  <HistoryPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/learning/revision/:sessionId"
            element={
              <ProtectedRoute>
                <Layout>
                  <RevisionPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Enhanced Features */}
          <Route
            path="/learn-from-anything"
            element={
              <ProtectedRoute>
                <Layout>
                  <LearnFromAnythingPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/reverse-classroom"
            element={
              <ProtectedRoute>
                <Layout>
                  <ReverseClassroomPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/time-travel"
            element={
              <ProtectedRoute>
                <Layout>
                  <TimeTravelPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/concept-collision"
            element={
              <ProtectedRoute>
                <Layout>
                  <ConceptCollisionPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/mistake-autopsy"
            element={
              <ProtectedRoute>
                <Layout>
                  <MistakeAutopsyPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/youtube-course"
            element={
              <ProtectedRoute>
                <Layout>
                  <YouTubeCoursePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/debate-arena"
            element={
              <ProtectedRoute>
                <Layout>
                  <DebateArenaPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dream-project"
            element={
              <ProtectedRoute>
                <Layout>
                  <DreamProjectPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/feynman"
            element={
              <ProtectedRoute>
                <Layout>
                  <FeynmanEnginePage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Admin routes */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <AdminHomePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/tournaments"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageTournamentsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/teams"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageTeamsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/questions"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageQuestionsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/users"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageUsersPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
