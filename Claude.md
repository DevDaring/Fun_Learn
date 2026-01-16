# Claude Implementation Guide for GenLearn AI

This document provides guidance for implementing the GenLearn AI prototype using Claude Code or Claude API.

## Overview

GenLearn AI is a full-stack Generative AI-enabled adaptive learning system with:
- **Frontend**: React 18 + Vite + TypeScript + Tailwind CSS
- **Backend**: Python 3.11+ with FastAPI
- **Database**: CSV files (pandas)
- **Storage**: Local file system for media

## Implementation Strategy

### Phase 1: Project Setup and Infrastructure
1. Create directory structure as specified in genlearn-ai-prompt.md
2. Initialize frontend with Vite + React + TypeScript
3. Set up FastAPI backend with proper folder structure
4. Create all CSV schemas with sample data
5. Set up environment configuration files

### Phase 2: API Provider Abstraction Layer
1. Implement base provider interfaces:
   - `backend/app/services/ai_providers/base.py`
   - `backend/app/services/image_providers/base.py`
   - `backend/app/services/voice_providers/base.py`
2. Implement ProviderFactory (single configuration point)
3. Implement Gemini provider as primary AI provider
4. Add fallback providers (OpenAI, Anthropic)
5. Implement FIBO image provider with Stability AI fallback
6. Implement GCP TTS/STT with Azure fallback

### Phase 3: Core Backend Services
1. CSV Handler with CRUD operations
2. File Handler for media management
3. Content Generation Service
4. Question Generation Service
5. Answer Evaluation Service
6. Video Generation Service (FFmpeg-based)
7. Avatar Service
8. Scoring Service

### Phase 4: Backend API Routes
Implement FastAPI routes in order:
1. Authentication (`/api/auth/*`)
2. Users (`/api/users/*`)
3. Learning Sessions (`/api/learning/*`)
4. Quiz (`/api/quiz/*`)
5. Avatar & Characters (`/api/avatar/*`, `/api/characters/*`)
6. Voice (`/api/voice/*`)
7. Video (`/api/video/*`)
8. Tournaments & Teams (`/api/tournaments/*`, `/api/teams/*`)
9. Chat (`/api/chat/*`)
10. Admin (`/api/admin/*`)

### Phase 5: Frontend Foundation
1. Set up routing with React Router
2. Create TypeScript types (`frontend/src/types/index.ts`)
3. Implement API service with Axios
4. Create Zustand stores for state management
5. Implement authentication flow
6. Create protected routes

### Phase 6: Frontend Layout & Common Components
1. Three-panel layout (TopNavbar, LeftMenu, MainContent, RightPanel)
2. Common components (Button, Modal, Dropdown, etc.)
3. Loading states and error handling
4. Toast notifications

### Phase 7: Core Frontend Features
1. **Login & Authentication**
   - LoginPage with form validation
   - Protected routes
   - User profile management

2. **Course Setup**
   - Topic input with AI suggestions
   - Difficulty slider (1-10)
   - Duration selection
   - Visual style selector
   - Play mode selector

3. **Learning Session**
   - Image carousel (3 images)
   - Story narratives with facts
   - Audio playback
   - Progress tracking

4. **Quiz System**
   - MCQ with 4 options
   - Descriptive questions with text input
   - Real-time feedback
   - Score calculation

5. **Video Generation**
   - Background generation
   - Status polling
   - Seamless playback

### Phase 8: Advanced Features
1. **Avatar System**
   - Drawing canvas (Fabric.js or React-Konva)
   - Image upload
   - Gallery selection
   - Avatar customization

2. **Character Management**
   - Character creation
   - Character selection for stories
   - Character gallery

3. **Voice Features**
   - Voice input (Web Speech API or mic recording)
   - Text-to-speech output
   - Full Vocal Mode
   - Multi-language support

4. **Gamification**
   - Team creation and management
   - Tournament system
   - Leaderboard
   - XP and leveling system
   - Streak tracking

### Phase 9: Admin Features
1. Admin dashboard
2. Tournament creation
3. Team management
4. Question upload (CSV)
5. User management

### Phase 10: Polish & Testing
1. Responsive design
2. Error handling and validation
3. Loading states
4. Accessibility features
5. Performance optimization
6. Cross-browser testing

## Key Implementation Details

### Provider Factory Pattern
The ProviderFactory is the SINGLE POINT where you switch providers by changing environment variables:

```python
# In .env file
AI_PROVIDER=gemini          # or openai, anthropic
IMAGE_PROVIDER=fibo         # or stability
VOICE_TTS_PROVIDER=gcp      # or azure
VOICE_STT_PROVIDER=gcp      # or azure
```

All services use the factory:
```python
from app.services.provider_factory import ProviderFactory

ai_provider = ProviderFactory.get_ai_provider()
image_provider = ProviderFactory.get_image_provider()
tts_provider = ProviderFactory.get_tts_provider()
stt_provider = ProviderFactory.get_stt_provider()
```

### CSV Database Operations
Use pandas for all CSV operations:
```python
import pandas as pd

def read_users():
    return pd.read_csv('data/csv/users.csv')

def add_user(user_data):
    df = read_users()
    new_row = pd.DataFrame([user_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('data/csv/users.csv', index=False)
```

### Learning Session Workflow
1. User configures course (topic, difficulty, duration, style)
2. Backend generates content using AI provider
3. Backend generates images using image provider
4. Frontend displays 3-image carousel with narratives
5. User views all images, then proceeds to quiz
6. Backend generates MCQ and descriptive questions
7. User answers questions, gets real-time feedback
8. Backend generates video asynchronously
9. Video plays after completion
10. Cycle repeats based on duration

### Adaptive Content Scaling
Duration determines number of cycles:
- 5 minutes = 1 cycle (3 images + quiz + video)
- 10 minutes = 2 cycles
- 15 minutes = 3 cycles
- 30 minutes = 6 cycles

Each cycle takes approximately 5 minutes.

### Full Vocal Mode
When enabled:
1. System announces all UI elements
2. Voice commands control navigation
3. Questions are read aloud
4. User answers via voice input
5. Feedback is spoken

Commands:
- "Start learning" - begins session
- "Next image" - advances carousel
- "Answer A/B/C/D" - selects MCQ option
- "Help" - provides guidance

### Video Generation Pipeline
1. Receive request with session_id and cycle_number
2. Create background task for video generation
3. Collect images from current cycle
4. Generate audio narration for each image
5. Use FFmpeg to compose:
   - Each image displays for 2-3 seconds
   - Corresponding audio plays over image
   - Smooth transitions between images
   - Total duration ~8 seconds
6. Save to `data/media/generated_videos/`
7. Update status to "ready"
8. Return video URL

## Best Practices

### Error Handling
- Always validate inputs
- Use try-except blocks for API calls
- Return meaningful error messages
- Log errors for debugging

### Security
- Hash passwords with bcrypt
- Use JWT tokens for authentication
- Validate all user inputs
- Prevent SQL injection (even with CSV)
- Sanitize file uploads

### Performance
- Use async/await for I/O operations
- Cache frequently accessed data
- Lazy load images
- Use pagination for large lists
- Optimize image sizes

### Code Organization
- Keep components small and focused
- Use custom hooks for reusable logic
- Separate business logic from UI
- Follow DRY principle
- Comment complex logic

## Testing Strategy

### Backend Testing
1. Test CSV operations (CRUD)
2. Test API provider integrations
3. Test authentication flow
4. Test each API endpoint
5. Test video generation pipeline

### Frontend Testing
1. Test component rendering
2. Test user interactions
3. Test form validation
4. Test API integration
5. Test state management

### Integration Testing
1. Test complete learning workflow
2. Test tournament participation
3. Test team collaboration
4. Test admin operations
5. Test voice features

## Deployment Considerations

### Environment Variables
Create `.env` file with all required API keys:
- GEMINI_API_KEY
- FIBO_API_KEY
- GCP_PROJECT_ID
- GCP_STT_API_KEY
- GCP_TTS_API_KEY
- SECRET_KEY (for JWT)

### Dependencies
Backend (requirements.txt):
- fastapi
- uvicorn
- pandas
- python-dotenv
- httpx
- bcrypt
- pydantic
- python-multipart
- pydub (optional)

Frontend (package.json):
- react
- react-router-dom
- axios
- zustand
- tailwindcss
- fabric or react-konva

### Running Locally
Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Prompting Claude for Implementation

### Effective Prompts

**For setting up project:**
```
Create the complete directory structure for GenLearn AI as specified in genlearn-ai-prompt.md.
Include all folders for frontend and backend, and create placeholder __init__.py files where needed.
```

**For implementing provider factory:**
```
Implement the ProviderFactory class in backend/app/services/provider_factory.py exactly as
specified in the prompt. Include all base provider interfaces and the Gemini provider implementation.
```

**For creating API routes:**
```
Implement the authentication routes in backend/app/api/routes/auth.py with:
1. POST /login - authenticate user and return JWT
2. GET /me - get current user info
3. POST /logout - invalidate token
Use the CSV handler for user data and bcrypt for password hashing.
```

**For creating frontend components:**
```
Create the CourseSetup component in frontend/src/components/learning/CourseSetup.tsx with:
1. Topic input field with placeholder text
2. Difficulty slider (1-10) with visual indicator
3. Duration dropdown (5, 10, 15, 30 mins)
4. Visual style toggle (cartoon/realistic)
5. Play mode selector (solo/team/tournament)
6. Start button that calls api.startSession()
Use Tailwind CSS for styling and TypeScript for type safety.
```

### Iteration Strategy

1. **Start with backend foundation** (CSV handlers, providers, basic routes)
2. **Create minimal frontend** (layout, routing, auth)
3. **Implement one complete feature** (e.g., learning session)
4. **Test end-to-end** before moving to next feature
5. **Iterate and refine** based on testing feedback

### Handling Complexity

Break down complex features into smaller tasks:

**Example: Video Generation**
1. Create video generation service structure
2. Implement image collection logic
3. Implement audio generation
4. Implement FFmpeg integration
5. Implement background task queue
6. Implement status endpoint
7. Test with sample data

## Common Challenges and Solutions

### Challenge: CSV file locking
**Solution**: Use file locking mechanisms or implement a simple queue for write operations

### Challenge: Async video generation
**Solution**: Use FastAPI BackgroundTasks or Celery for task queue

### Challenge: Voice input in browser
**Solution**: Use Web Speech API for modern browsers, provide fallback for unsupported browsers

### Challenge: Image generation latency
**Solution**: Generate images asynchronously, show loading states, cache generated images

### Challenge: State management in frontend
**Solution**: Use Zustand for global state, React Context for theme/settings, local state for UI

## Success Criteria

The prototype is complete when:
- [ ] User can register/login successfully
- [ ] User can configure and start a learning session
- [ ] 3 images are generated and displayed with narratives
- [ ] Quiz questions are generated based on content
- [ ] MCQ answers are validated correctly
- [ ] Descriptive answers are evaluated by AI
- [ ] Video is generated and played
- [ ] User can create avatar (draw/upload/gallery)
- [ ] User can add characters to stories
- [ ] Voice input and output work
- [ ] Full Vocal Mode is functional
- [ ] Teams can be created and joined
- [ ] Tournaments can be created by admin
- [ ] Leaderboard displays correctly
- [ ] Admin can upload questions via CSV
- [ ] All API providers are swappable via env vars

## Conclusion

This prototype demonstrates a complete AI-powered adaptive learning system. Follow the phased approach, implement features incrementally, test thoroughly, and iterate based on feedback. The modular architecture allows for easy extension and provider switching.
