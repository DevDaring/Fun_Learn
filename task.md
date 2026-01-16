# GenLearn AI Implementation Task List

This document breaks down the GenLearn AI prototype implementation into manageable tasks.

## Phase 1: Project Setup (Foundation)

### 1.1 Directory Structure
- [ ] Create complete folder structure for frontend
- [ ] Create complete folder structure for backend
- [ ] Create data folders for CSV and media
- [ ] Add `.gitignore` for both frontend and backend
- [ ] Create README.md with project overview

### 1.2 Backend Setup
- [ ] Initialize Python virtual environment
- [ ] Create `requirements.txt` with all dependencies
- [ ] Set up FastAPI app structure
- [ ] Create `backend/app/main.py` with CORS middleware
- [ ] Create `backend/app/config.py` for settings
- [ ] Create environment template in `docs/env.md`
- [ ] Create `.env` file with placeholder values

### 1.3 Frontend Setup
- [ ] Initialize Vite + React + TypeScript project
- [ ] Install dependencies (axios, zustand, react-router-dom)
- [ ] Configure Tailwind CSS
- [ ] Create `frontend/src/types/index.ts` with all TypeScript types
- [ ] Create basic folder structure for components
- [ ] Set up routing in `App.tsx`

### 1.4 CSV Database Setup
- [ ] Create `data/csv/users.csv` with sample data
- [ ] Create `data/csv/sessions.csv` with sample data
- [ ] Create `data/csv/scores.csv` with sample data
- [ ] Create `data/csv/questions_mcq.csv` with sample data
- [ ] Create `data/csv/questions_descriptive.csv` with sample data
- [ ] Create `data/csv/tournaments.csv` with sample data
- [ ] Create `data/csv/teams.csv` with sample data
- [ ] Create `data/csv/team_members.csv` with sample data
- [ ] Create `data/csv/avatars.csv` with sample data
- [ ] Create `data/csv/characters.csv` with sample data
- [ ] Create `data/csv/learning_history.csv` with sample data

---

## Phase 2: API Provider Abstraction Layer

### 2.1 Base Provider Interfaces
- [ ] Create `backend/app/services/ai_providers/base.py`
- [ ] Define BaseAIProvider abstract class
- [ ] Define ContentGenerationRequest model
- [ ] Define QuestionGenerationRequest model
- [ ] Define AnswerEvaluationRequest model
- [ ] Create `backend/app/services/image_providers/base.py`
- [ ] Define BaseImageProvider abstract class
- [ ] Define ImageGenerationRequest model
- [ ] Create `backend/app/services/voice_providers/base.py`
- [ ] Define BaseTTSProvider abstract class
- [ ] Define BaseSTTProvider abstract class

### 2.2 Provider Factory
- [ ] Create `backend/app/services/provider_factory.py`
- [ ] Implement `get_ai_provider()` method
- [ ] Implement `get_image_provider()` method
- [ ] Implement `get_tts_provider()` method
- [ ] Implement `get_stt_provider()` method
- [ ] Implement `get_all_providers()` method
- [ ] Implement `check_all_providers()` health check

### 2.3 Gemini Provider (Primary AI)
- [ ] Create `backend/app/services/ai_providers/gemini.py`
- [ ] Implement Gemini API client initialization
- [ ] Implement `generate_content()` method
- [ ] Implement `generate_mcq_questions()` method
- [ ] Implement `generate_descriptive_questions()` method
- [ ] Implement `evaluate_answer()` method
- [ ] Implement `chat()` method
- [ ] Implement `health_check()` method
- [ ] Add JSON response parsing and cleaning

### 2.4 FIBO Image Provider (Primary)
- [ ] Create `backend/app/services/image_providers/fibo.py`
- [ ] Implement FIBO API client
- [ ] Implement `generate_image()` method
- [ ] Implement `generate_avatar()` method
- [ ] Implement `stylize_character()` method
- [ ] Implement `health_check()` method

### 2.5 GCP Voice Providers (Primary)
- [ ] Create `backend/app/services/voice_providers/gcp_tts.py`
- [ ] Implement GCP Text-to-Speech client
- [ ] Implement `synthesize_speech()` method
- [ ] Implement `get_supported_languages()` method
- [ ] Create `backend/app/services/voice_providers/gcp_stt.py`
- [ ] Implement GCP Speech-to-Text client
- [ ] Implement `transcribe_audio()` method
- [ ] Implement language support methods

### 2.6 Fallback Providers (Optional)
- [ ] Create `backend/app/services/ai_providers/openai.py`
- [ ] Create `backend/app/services/ai_providers/anthropic.py`
- [ ] Create `backend/app/services/image_providers/stability.py`
- [ ] Create `backend/app/services/voice_providers/azure_voice.py`

---

## Phase 3: Core Backend Services

### 3.1 Database Handlers
- [ ] Create `backend/app/database/csv_handler.py`
- [ ] Implement `read_csv()` function
- [ ] Implement `write_csv()` function
- [ ] Implement `append_csv()` function
- [ ] Implement `update_csv()` function
- [ ] Implement `delete_from_csv()` function
- [ ] Implement auto-ID generation
- [ ] Add file locking mechanism

### 3.2 File Handler
- [ ] Create `backend/app/database/file_handler.py`
- [ ] Implement `save_file()` function
- [ ] Implement `get_file_url()` function
- [ ] Implement `delete_file()` function
- [ ] Implement unique filename generation
- [ ] Add file type validation

### 3.3 Content Generation Service
- [ ] Create `backend/app/services/content_generator.py`
- [ ] Implement `generate_learning_content()` function
- [ ] Implement story segment creation
- [ ] Implement image prompt generation
- [ ] Integrate with AI provider
- [ ] Integrate with image provider
- [ ] Add error handling and retries

### 3.4 Question Generation Service
- [ ] Create `backend/app/services/question_generator.py`
- [ ] Implement `generate_mcq_questions()` function
- [ ] Implement `generate_descriptive_questions()` function
- [ ] Integrate with AI provider
- [ ] Save questions to CSV

### 3.5 Answer Evaluation Service
- [ ] Create `backend/app/services/answer_evaluator.py`
- [ ] Implement `evaluate_mcq_answer()` function
- [ ] Implement `evaluate_descriptive_answer()` function
- [ ] Implement scoring logic
- [ ] Save scores to CSV

### 3.6 Video Generation Service
- [ ] Create `backend/app/services/video_generator.py`
- [ ] Implement image collection logic
- [ ] Implement audio generation for narration
- [ ] Implement FFmpeg video composition
- [ ] Implement background task queue
- [ ] Implement status tracking
- [ ] Save videos to media folder

### 3.7 Avatar Service
- [ ] Create `backend/app/services/avatar_service.py`
- [ ] Implement avatar creation from upload
- [ ] Implement avatar creation from drawing
- [ ] Implement avatar gallery selection
- [ ] Integrate with image provider
- [ ] Save avatars to CSV and media folder

### 3.8 Scoring Service
- [ ] Create `backend/app/services/scoring_service.py`
- [ ] Implement XP calculation logic
- [ ] Implement level calculation
- [ ] Implement streak tracking
- [ ] Update user scores in CSV

### 3.9 Data Models
- [ ] Create `backend/app/models/user.py`
- [ ] Create `backend/app/models/session.py`
- [ ] Create `backend/app/models/quiz.py`
- [ ] Create `backend/app/models/tournament.py`
- [ ] Create `backend/app/models/team.py`
- [ ] Create `backend/app/models/avatar.py`

---

## Phase 4: Backend API Routes

### 4.1 Authentication Routes
- [ ] Create `backend/app/api/routes/auth.py`
- [ ] Implement `POST /api/auth/login` endpoint
- [ ] Implement `GET /api/auth/me` endpoint
- [ ] Implement `POST /api/auth/logout` endpoint
- [ ] Add JWT token generation
- [ ] Add password hashing with bcrypt
- [ ] Create `backend/app/api/dependencies.py` for auth middleware

### 4.2 User Routes
- [ ] Create `backend/app/api/routes/users.py`
- [ ] Implement `GET /api/users/profile` endpoint
- [ ] Implement `PUT /api/users/profile` endpoint
- [ ] Implement `GET /api/users/history` endpoint
- [ ] Implement `PUT /api/users/settings` endpoint

### 4.3 Learning Routes
- [ ] Create `backend/app/api/routes/learning.py`
- [ ] Implement `POST /api/learning/start` endpoint
- [ ] Implement `GET /api/learning/session/{id}/content` endpoint
- [ ] Implement `POST /api/learning/session/{id}/progress` endpoint
- [ ] Implement `POST /api/learning/session/{id}/end` endpoint
- [ ] Integrate with content generation service

### 4.4 Quiz Routes
- [ ] Create `backend/app/api/routes/quiz.py`
- [ ] Implement `GET /api/quiz/session/{id}/mcq` endpoint
- [ ] Implement `POST /api/quiz/session/{id}/mcq/answer` endpoint
- [ ] Implement `GET /api/quiz/session/{id}/descriptive` endpoint
- [ ] Implement `POST /api/quiz/session/{id}/descriptive/answer` endpoint
- [ ] Integrate with question generator and answer evaluator

### 4.5 Avatar Routes
- [ ] Create `backend/app/api/routes/avatar.py`
- [ ] Implement `GET /api/avatar/list` endpoint
- [ ] Implement `POST /api/avatar/upload` endpoint
- [ ] Implement `POST /api/avatar/draw` endpoint
- [ ] Implement `GET /api/avatar/gallery` endpoint
- [ ] Integrate with avatar service

### 4.6 Character Routes
- [ ] Create `backend/app/api/routes/characters.py`
- [ ] Implement `GET /api/characters/list` endpoint
- [ ] Implement `POST /api/characters/create` endpoint
- [ ] Implement `DELETE /api/characters/{id}` endpoint
- [ ] Integrate with image provider

### 4.7 Voice Routes
- [ ] Create `backend/app/api/routes/voice.py`
- [ ] Implement `POST /api/voice/tts` endpoint
- [ ] Implement `POST /api/voice/stt` endpoint
- [ ] Integrate with voice providers
- [ ] Handle audio file uploads

### 4.8 Video Routes
- [ ] Create `backend/app/api/routes/video.py`
- [ ] Implement `GET /api/video/session/{id}/cycle/{n}` endpoint
- [ ] Implement `GET /api/video/session/{id}/cycle/{n}/status` endpoint
- [ ] Integrate with video generation service

### 4.9 Tournament Routes
- [ ] Create `backend/app/api/routes/tournaments.py`
- [ ] Implement `GET /api/tournaments/list` endpoint
- [ ] Implement `POST /api/tournaments/{id}/join` endpoint
- [ ] Implement `GET /api/tournaments/leaderboard` endpoint
- [ ] Implement tournament status logic

### 4.10 Team Routes
- [ ] Create `backend/app/api/routes/teams.py`
- [ ] Implement `GET /api/teams/list` endpoint
- [ ] Implement `POST /api/teams/create` endpoint
- [ ] Implement `POST /api/teams/{id}/join` endpoint
- [ ] Implement `GET /api/teams/{id}` endpoint

### 4.11 Chat Routes
- [ ] Create `backend/app/api/routes/chat.py`
- [ ] Implement `POST /api/chat/message` endpoint
- [ ] Integrate with AI provider chat method
- [ ] Support multi-language chat

### 4.12 Admin Routes
- [ ] Create `backend/app/api/routes/admin.py`
- [ ] Implement `POST /api/admin/tournaments/create` endpoint
- [ ] Implement `POST /api/admin/questions/upload` endpoint
- [ ] Implement `GET /api/admin/users` endpoint
- [ ] Add admin authorization checks

---

## Phase 5: Frontend Foundation

### 5.1 API Service Layer
- [ ] Create `frontend/src/services/api.ts`
- [ ] Implement Axios client configuration
- [ ] Add request interceptor for auth token
- [ ] Add response interceptor for error handling
- [ ] Implement all auth methods
- [ ] Implement all learning methods
- [ ] Implement all quiz methods
- [ ] Implement all avatar/character methods
- [ ] Implement all voice methods
- [ ] Implement all video methods
- [ ] Implement all tournament/team methods
- [ ] Implement all chat methods
- [ ] Implement all admin methods

### 5.2 State Management
- [ ] Create `frontend/src/store/authStore.ts`
- [ ] Create `frontend/src/store/learningStore.ts`
- [ ] Create `frontend/src/store/settingsStore.ts`
- [ ] Create `frontend/src/store/voiceStore.ts`
- [ ] Implement auth state management
- [ ] Implement learning session state
- [ ] Implement settings state
- [ ] Implement voice settings state

### 5.3 Custom Hooks
- [ ] Create `frontend/src/hooks/useAuth.ts`
- [ ] Create `frontend/src/hooks/useVoice.ts`
- [ ] Create `frontend/src/hooks/useLearningSession.ts`
- [ ] Create `frontend/src/hooks/useFullVocalMode.ts`
- [ ] Create `frontend/src/hooks/useApi.ts`
- [ ] Implement authentication logic
- [ ] Implement voice recording logic
- [ ] Implement session management logic

### 5.4 Routing
- [ ] Configure React Router in `App.tsx`
- [ ] Define all page routes
- [ ] Implement protected route wrapper
- [ ] Add route-based code splitting
- [ ] Add 404 page

---

## Phase 6: Frontend Layout & Common Components

### 6.1 Layout Components
- [ ] Create `frontend/src/components/layout/TopNavbar.tsx`
- [ ] Create `frontend/src/components/layout/LeftMenu.tsx`
- [ ] Create `frontend/src/components/layout/RightPanel.tsx`
- [ ] Create `frontend/src/components/layout/MainContent.tsx`
- [ ] Create `frontend/src/components/layout/Layout.tsx`
- [ ] Implement responsive three-panel layout
- [ ] Add navigation menu items
- [ ] Add user profile dropdown

### 6.2 Common UI Components
- [ ] Create `frontend/src/components/common/Button.tsx`
- [ ] Create `frontend/src/components/common/Modal.tsx`
- [ ] Create `frontend/src/components/common/Dropdown.tsx`
- [ ] Create `frontend/src/components/common/Slider.tsx`
- [ ] Create `frontend/src/components/common/LoadingSpinner.tsx`
- [ ] Create `frontend/src/components/common/ProgressBar.tsx`
- [ ] Create `frontend/src/components/common/Toast.tsx`
- [ ] Style with Tailwind CSS
- [ ] Add accessibility attributes

---

## Phase 7: Core Frontend Features

### 7.1 Authentication Pages
- [ ] Create `frontend/src/pages/LoginPage.tsx`
- [ ] Create `frontend/src/components/auth/LoginForm.tsx`
- [ ] Create `frontend/src/components/auth/ProtectedRoute.tsx`
- [ ] Implement login form with validation
- [ ] Implement error handling
- [ ] Add "Remember me" functionality
- [ ] Redirect after successful login

### 7.2 Dashboard Page
- [ ] Create `frontend/src/pages/DashboardPage.tsx`
- [ ] Display user stats (XP, level, streak)
- [ ] Show recent learning history
- [ ] Display available tournaments
- [ ] Add quick start button

### 7.3 Course Setup
- [ ] Create `frontend/src/pages/LearningPage.tsx`
- [ ] Create `frontend/src/components/learning/CourseSetup.tsx`
- [ ] Implement topic input field
- [ ] Implement difficulty slider (1-10)
- [ ] Implement duration dropdown
- [ ] Implement visual style toggle
- [ ] Implement play mode selector
- [ ] Add start button with loading state

### 7.4 Learning Session
- [ ] Create `frontend/src/components/learning/LearningSession.tsx`
- [ ] Create `frontend/src/components/learning/ImageCard.tsx`
- [ ] Create `frontend/src/components/learning/ImageCarousel.tsx`
- [ ] Implement 3-image carousel
- [ ] Display narratives and facts
- [ ] Add audio playback button
- [ ] Show progress indicator
- [ ] Add next/previous navigation

### 7.5 Quiz Components
- [ ] Create `frontend/src/components/learning/MCQQuiz.tsx`
- [ ] Create `frontend/src/components/learning/DescriptiveQuestion.tsx`
- [ ] Implement MCQ with 4 options
- [ ] Implement visual background for MCQ
- [ ] Implement text area for descriptive answers
- [ ] Show immediate feedback after submission
- [ ] Display score and explanation
- [ ] Add timer (optional)

### 7.6 Video Player
- [ ] Create `frontend/src/components/learning/VideoPlayer.tsx`
- [ ] Implement video status polling
- [ ] Show loading state during generation
- [ ] Implement video playback controls
- [ ] Add replay functionality
- [ ] Handle video errors gracefully

---

## Phase 8: Advanced Features

### 8.1 Avatar System
- [ ] Create `frontend/src/pages/AvatarPage.tsx`
- [ ] Create `frontend/src/components/avatar/AvatarCreator.tsx`
- [ ] Create `frontend/src/components/avatar/DrawingCanvas.tsx`
- [ ] Create `frontend/src/components/avatar/ImageUploader.tsx`
- [ ] Create `frontend/src/components/avatar/AvatarGallery.tsx`
- [ ] Implement drawing canvas with Fabric.js or React-Konva
- [ ] Implement image upload with preview
- [ ] Implement gallery selection
- [ ] Add avatar style selector
- [ ] Add save/cancel buttons

### 8.2 Character Management
- [ ] Create `frontend/src/pages/CharactersPage.tsx`
- [ ] Create `frontend/src/components/characters/CharacterManager.tsx`
- [ ] Create `frontend/src/components/characters/CharacterCard.tsx`
- [ ] Display character gallery
- [ ] Implement character creation form
- [ ] Add character selection for stories
- [ ] Add delete functionality

### 8.3 Voice Features
- [ ] Create `frontend/src/components/voice/VoiceInput.tsx`
- [ ] Create `frontend/src/components/voice/VoiceOutput.tsx`
- [ ] Create `frontend/src/components/voice/FullVocalMode.tsx`
- [ ] Create `frontend/src/components/voice/LanguageSelector.tsx`
- [ ] Implement microphone recording
- [ ] Implement Web Speech API integration
- [ ] Implement audio playback
- [ ] Implement Full Vocal Mode toggle
- [ ] Add voice command parsing
- [ ] Support multiple languages

### 8.4 Gamification - Teams
- [ ] Create `frontend/src/pages/LeaderboardPage.tsx`
- [ ] Create `frontend/src/components/gamification/Scoreboard.tsx`
- [ ] Create `frontend/src/components/gamification/TeamSelector.tsx`
- [ ] Display team leaderboard
- [ ] Implement team creation form
- [ ] Implement team join functionality
- [ ] Show team members

### 8.5 Gamification - Tournaments
- [ ] Create `frontend/src/pages/TournamentsPage.tsx`
- [ ] Create `frontend/src/components/gamification/TournamentList.tsx`
- [ ] Create `frontend/src/components/gamification/TournamentCard.tsx`
- [ ] Display upcoming tournaments
- [ ] Display active tournaments
- [ ] Display completed tournaments
- [ ] Implement tournament join functionality
- [ ] Show tournament leaderboard
- [ ] Display prizes

### 8.6 Chat Feature
- [ ] Create `frontend/src/components/chat/ChatWindow.tsx`
- [ ] Create `frontend/src/components/chat/ChatMessage.tsx`
- [ ] Implement chat interface in right panel
- [ ] Add message input field
- [ ] Display chat history
- [ ] Support multi-language chat
- [ ] Add chat with context (current lesson)

---

## Phase 9: Admin Features

### 9.1 Admin Dashboard
- [ ] Create `frontend/src/pages/admin/AdminHomePage.tsx`
- [ ] Create `frontend/src/components/admin/AdminDashboard.tsx`
- [ ] Display admin statistics
- [ ] Show recent user activity
- [ ] Add quick action buttons
- [ ] Implement admin navigation

### 9.2 Tournament Management
- [ ] Create `frontend/src/pages/admin/ManageTournamentsPage.tsx`
- [ ] Create `frontend/src/components/admin/TournamentCreator.tsx`
- [ ] Implement tournament creation form
- [ ] Add tournament list with edit/delete
- [ ] Add tournament status management
- [ ] Show participant list

### 9.3 Team Management
- [ ] Create `frontend/src/pages/admin/ManageTeamsPage.tsx`
- [ ] Create `frontend/src/components/admin/TeamManager.tsx`
- [ ] Display all teams
- [ ] Add team editing capabilities
- [ ] Add member management
- [ ] Show team statistics

### 9.4 Question Upload
- [ ] Create `frontend/src/pages/admin/ManageQuestionsPage.tsx`
- [ ] Create `frontend/src/components/admin/QuestionUploader.tsx`
- [ ] Implement CSV file upload
- [ ] Add file validation
- [ ] Show upload progress
- [ ] Display success/error messages
- [ ] Add question preview

### 9.5 User Management
- [ ] Create `frontend/src/pages/admin/ManageUsersPage.tsx`
- [ ] Create `frontend/src/components/admin/UserManager.tsx`
- [ ] Display all users
- [ ] Add user search/filter
- [ ] Implement user role management
- [ ] Show user activity

---

## Phase 10: Polish & Testing

### 10.1 Styling & Responsiveness
- [ ] Apply Tailwind CSS to all components
- [ ] Ensure mobile responsiveness
- [ ] Test on different screen sizes
- [ ] Add dark mode support (optional)
- [ ] Polish animations and transitions
- [ ] Optimize image loading

### 10.2 Error Handling
- [ ] Add error boundaries in React
- [ ] Implement global error handler
- [ ] Add user-friendly error messages
- [ ] Implement retry logic for failed API calls
- [ ] Add fallback UI for errors

### 10.3 Loading States
- [ ] Add loading spinners to all async operations
- [ ] Implement skeleton screens
- [ ] Add progress indicators for long operations
- [ ] Show loading states in buttons

### 10.4 Accessibility
- [ ] Add ARIA labels to all interactive elements
- [ ] Ensure keyboard navigation works
- [ ] Test screen reader compatibility
- [ ] Add focus indicators
- [ ] Ensure color contrast meets WCAG standards

### 10.5 Performance Optimization
- [ ] Implement code splitting
- [ ] Optimize image sizes
- [ ] Add caching for API responses
- [ ] Lazy load components
- [ ] Minimize bundle size

### 10.6 Testing
- [ ] Test user registration and login
- [ ] Test complete learning workflow
- [ ] Test quiz functionality
- [ ] Test video generation
- [ ] Test avatar creation
- [ ] Test team and tournament features
- [ ] Test admin features
- [ ] Test voice features
- [ ] Test error scenarios
- [ ] Test on multiple browsers

### 10.7 Documentation
- [ ] Update README.md with setup instructions
- [ ] Document environment variables
- [ ] Add API documentation
- [ ] Create user guide
- [ ] Add developer notes

---

## Phase 11: Final Deployment Preparation

### 11.1 Environment Configuration
- [ ] Set up production .env file
- [ ] Configure API keys for production
- [ ] Set up CORS for production domain
- [ ] Configure file upload limits
- [ ] Set up logging

### 11.2 Build and Deploy
- [ ] Build frontend for production
- [ ] Test production build locally
- [ ] Set up backend server
- [ ] Deploy frontend to hosting service
- [ ] Deploy backend to hosting service
- [ ] Configure domain and SSL
- [ ] Test deployed application

### 11.3 Post-Deployment
- [ ] Monitor error logs
- [ ] Monitor API usage
- [ ] Gather user feedback
- [ ] Plan for future enhancements
- [ ] Create backup strategy for CSV data

---

## Estimated Timeline

- **Phase 1-2**: 2-3 days (Setup and provider abstraction)
- **Phase 3-4**: 3-4 days (Backend services and API routes)
- **Phase 5-6**: 2 days (Frontend foundation and layout)
- **Phase 7**: 3-4 days (Core features)
- **Phase 8**: 3-4 days (Advanced features)
- **Phase 9**: 2 days (Admin features)
- **Phase 10**: 2-3 days (Polish and testing)
- **Phase 11**: 1 day (Deployment)

**Total Estimated Time**: 18-25 days for a complete prototype

---

## Priority Features (MVP)

If time is limited, prioritize these features for a minimal viable prototype:

1. **Must Have**:
   - User login/authentication
   - Course setup (topic, difficulty, duration)
   - 3-image carousel with narratives
   - MCQ quiz with feedback
   - Basic scoring
   - Solo play mode

2. **Should Have**:
   - Descriptive questions with AI evaluation
   - Video generation
   - Avatar creation (at least gallery selection)
   - Learning history
   - Basic leaderboard

3. **Nice to Have**:
   - Voice input/output
   - Full Vocal Mode
   - Teams and tournaments
   - Character management
   - Admin dashboard
   - Chat feature

---

## Notes

- Test each phase thoroughly before moving to the next
- Use sample API keys for development
- Create mock data for testing when API providers are not available
- Focus on core learning workflow first, then add gamification
- Ensure provider factory works before implementing all providers
- Keep code modular and well-documented
- Follow the exact structure specified in genlearn-ai-prompt.md
