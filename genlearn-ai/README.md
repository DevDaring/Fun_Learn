# GenLearn AI - Complete Prototype

**A Generative AI-Enabled Adaptive Learning System**

Full-stack application with React + TypeScript frontend and Python FastAPI backend, using CSV files for data storage and local folders for multimedia assets.

## 🎯 Project Overview

GenLearn AI is an intelligent learning platform that uses AI to:
- Generate personalized learning content with storytelling
- Create visual learning materials (images and videos)
- Evaluate student answers with detailed feedback
- Provide voice-based interaction (TTS/STT)
- Gamify learning with teams, tournaments, and leaderboards
- Support multiple languages and accessibility features

## 📁 Project Structure

```
genlearn-ai/
├── backend/              # Python FastAPI Backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── services/     # Business logic & AI providers
│   │   ├── database/     # CSV handlers
│   │   ├── models/       # Pydantic models
│   │   └── utils/        # Helper functions
│   ├── data/
│   │   ├── csv/          # CSV database files
│   │   └── media/        # Images, videos, audio files
│   └── requirements.txt
│
└── frontend/             # React + TypeScript Frontend
    ├── src/
    │   ├── components/   # Reusable React components
    │   ├── pages/        # Page components
    │   ├── hooks/        # Custom React hooks
    │   ├── services/     # API service layer
    │   ├── store/        # Zustand state management
    │   ├── types/        # TypeScript types
    │   └── utils/        # Utilities
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **API Keys** (see Environment Setup below)

### Backend Setup

```bash
# Navigate to backend directory
cd genlearn-ai/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your API keys
copy .env.example .env  # Windows
# or
cp .env.example .env    # macOS/Linux

# Edit .env file with your API keys

# Run the backend server
python run.py --reload

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd genlearn-ai/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Application will open at http://localhost:5173
```

## 🔑 Environment Setup

Create a `.env` file in the `backend/` directory with the following variables:

```env
# App Settings
APP_NAME=GenLearn AI
APP_ENV=development
DEBUG=true
SECRET_KEY=your_secret_key_change_in_production

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# Provider Selection (Change these to switch providers!)
AI_PROVIDER=gemini          # Options: gemini, openai, anthropic
IMAGE_PROVIDER=fibo         # Options: fibo, stability
VOICE_TTS_PROVIDER=gcp      # Options: gcp, azure
VOICE_STT_PROVIDER=gcp      # Options: gcp, azure

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# Google Cloud Platform
GCP_PROJECT_ID=your_gcp_project_id
GCP_STT_API_KEY=your_gcp_stt_api_key
GCP_TTS_API_KEY=your_gcp_tts_api_key

# FIBO API (Image Generation)
FIBO_API_KEY=your_fibo_api_key_here
FIBO_API_ENDPOINT=https://api.fibo.ai/v1

# Fallback Providers (Optional)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
STABILITY_API_KEY=your_stability_api_key_here
```

## 🎓 Default User Credentials

The application comes with pre-configured test users:

| Role  | Username      | Password     |
|-------|---------------|--------------|
| Admin | admin         | password123  |
| User  | john_doe      | password123  |
| User  | priya_sharma  | password123  |
| User  | amit_roy      | password123  |
| User  | sarah_wilson  | password123  |

## ✨ Features

### Core Learning Features
- ✅ **Adaptive Content Generation** - AI generates personalized learning content
- ✅ **Story-Based Learning** - Engaging narratives with visual elements
- ✅ **3-Image Carousel** - Visual learning with facts and narratives
- ✅ **AI-Generated Images** - Custom images for each learning segment
- ✅ **Video Generation** - 8-second educational videos from images
- ✅ **MCQ Questions** - Auto-generated multiple choice questions
- ✅ **Descriptive Questions** - Open-ended questions with AI evaluation
- ✅ **Adaptive Difficulty** - Content scales based on difficulty level (1-10)

### Avatar & Characters
- ✅ **Avatar Creation** - Draw, upload, or choose from gallery
- ✅ **Character System** - Add custom characters to stories
- ✅ **Style Options** - Cartoon or realistic visual styles

### Voice Features
- ✅ **Text-to-Speech** - Narration for all content
- ✅ **Speech-to-Text** - Voice input for answers
- ✅ **Full Vocal Mode** - Complete hands-free operation
- ✅ **Multi-Language** - Support for 8+ languages

### Gamification
- ✅ **XP & Leveling System** - Progress tracking
- ✅ **Streak Tracking** - Daily learning streaks
- ✅ **Teams** - Create and join learning teams
- ✅ **Tournaments** - Competitive learning events
- ✅ **Leaderboards** - Global and tournament rankings

### Admin Features
- ✅ **Tournament Management** - Create and manage tournaments
- ✅ **Question Upload** - Bulk upload via CSV
- ✅ **User Management** - View and manage users
- ✅ **Team Management** - Oversee team activities
- ✅ **Analytics Dashboard** - Key metrics and insights

## 🔌 API Provider Switching

The application uses a **Provider Factory Pattern** for easy switching between AI providers. Simply change environment variables - **no code changes required!**

### Switching AI Provider
```env
AI_PROVIDER=gemini      # or: openai, anthropic
```

### Switching Image Provider
```env
IMAGE_PROVIDER=fibo     # or: stability
```

### Switching Voice Providers
```env
VOICE_TTS_PROVIDER=gcp  # or: azure
VOICE_STT_PROVIDER=gcp  # or: azure
```

## 📊 CSV Database Schema

The application uses CSV files for data storage:

- **users.csv** - User accounts and profiles
- **sessions.csv** - Learning sessions
- **scores.csv** - Quiz scores and results
- **questions_mcq.csv** - Multiple choice questions
- **questions_descriptive.csv** - Descriptive questions
- **tournaments.csv** - Tournament data
- **teams.csv** - Team information
- **team_members.csv** - Team membership
- **avatars.csv** - User avatars
- **characters.csv** - Custom characters
- **learning_history.csv** - Learning activity history

## 🎨 Frontend Technology Stack

- **Framework**: React 18 + Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Drawing**: Fabric.js
- **Audio**: Web Audio API

## 🔧 Backend Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: CSV files (pandas)
- **File Storage**: Local filesystem
- **API Integration**: httpx (async)
- **Authentication**: JWT + bcrypt
- **Validation**: Pydantic
- **Image Processing**: Pillow
- **Audio**: pydub

## 🏗️ Architecture Highlights

### Provider Abstraction Layer
All AI, Image, and Voice providers are abstracted through a factory pattern, allowing seamless switching between providers without code changes.

### Service Layer
Business logic is separated into services:
- `ContentGenerator` - Generates learning content
- `QuestionGenerator` - Creates quiz questions
- `AnswerEvaluator` - Evaluates student answers
- `VideoGenerator` - Creates educational videos
- `AvatarService` - Manages avatar creation
- `ScoringService` - Handles XP and scoring

### Three-Panel Layout
The frontend uses a consistent three-panel layout:
- **Left Panel**: Navigation menu
- **Main Panel**: Primary content area
- **Right Panel**: Chat assistant / contextual info

## 📖 Documentation

- **Backend API**: Visit `http://localhost:8000/docs` when backend is running
- **Backend README**: See `backend/README.md`
- **API Documentation**: See `backend/API_DOCUMENTATION.md`
- **Provider Guide**: See `backend/PROVIDERS_README.md`
- **Quick Start**: See `backend/QUICK_START.md`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python verify_installation.py
```

### Frontend Testing
```bash
cd frontend
npm run build  # Verify build succeeds
```

## 📝 Sample Workflow

1. **User logs in** with credentials (john_doe / password123)
2. **Configures course**:
   - Topic: "Photosynthesis"
   - Difficulty: 5
   - Duration: 15 minutes
   - Visual Style: Cartoon
   - Play Mode: Solo
3. **Views learning content**:
   - 3 AI-generated images with narratives
   - Facts about photosynthesis
   - Audio narration
4. **Watches video**: 8-second educational video
5. **Takes quiz**:
   - 3 MCQ questions
   - 3 descriptive questions
6. **Receives feedback**: AI evaluates answers with detailed feedback
7. **Earns XP**: Gains experience points and levels up
8. **Views leaderboard**: Compares score with others

## 🚀 Production Deployment

### Backend Deployment
- Use `gunicorn` or `uvicorn` with multiple workers
- Set `DEBUG=false` in production
- Use proper secrets management (not .env file)
- Set up proper file backups for CSV data
- Consider migrating to a real database (PostgreSQL/MongoDB)

### Frontend Deployment
```bash
npm run build
# Deploy the `dist/` folder to your hosting service
```

Popular hosting options:
- **Vercel** (frontend)
- **Heroku** (backend)
- **AWS** (full stack)
- **DigitalOcean** (full stack)

## 🤝 Contributing

This is a prototype project. For production use:
1. Replace CSV storage with a proper database
2. Implement proper authentication (OAuth, 2FA)
3. Add rate limiting and caching
4. Implement comprehensive logging
5. Add automated testing
6. Set up CI/CD pipeline

## 📄 License

This is a prototype project for educational purposes.

## 🙏 Acknowledgments

Built with:
- FastAPI
- React
- Tailwind CSS
- Google Gemini AI
- FIBO API
- Google Cloud Platform

## 📞 Support

For issues or questions, please refer to:
- Backend documentation in `backend/README.md`
- API documentation at `http://localhost:8000/docs`
- Frontend code comments for component usage

---

**Made with ❤️ for adaptive learning**

Last Updated: December 2024
Version: 1.0.0-prototype
