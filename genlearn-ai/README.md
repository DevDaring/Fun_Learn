# 🎓 Fun Learn

<div align="center">

**🏆 Built for Google Gemini 3 Hackathon**

*Where AI Becomes Your Student, Not Your Teacher*

[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%203-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

</div>

---

## 🎯 The Problem

**1.5 million students fail board exams in India every year.** Not because they're not smart enough — because passive learning doesn't work. Reading textbooks, watching videos, memorizing answers — it's broken.

## 💡 Our Solution

**Fun Learn** flips the script. Instead of AI teaching students, **students teach the AI**. This activates the Feynman Technique at scale, powered by Gemini's multimodal capabilities.

---

## ✨ Core Innovation: The Feynman Engine

The Feynman Technique states: *"If you can't explain it simply, you don't understand it well enough."*

We built **Ritty** — an AI-powered curious 8-year-old who asks "Why?" until you truly understand.

| Layer | Name | How It Works |
|-------|------|--------------|
| 🧒 **Layer 1** | Teach Ritty | Explain any concept to an AI child who asks probing questions |
| 📦 **Layer 2** | Compression Challenge | Compress your explanation: 50 words → 25 → 10 |
| 🌀 **Layer 3** | The Why Spiral | Ritty asks "Why?" up to 5 levels deep |
| 🔗 **Layer 4** | Analogy Workshop | Create and defend analogies for concepts |
| 🎓 **Layer 5** | Lecture Hall | Explain to 5 personas simultaneously |

---

## 🚀 8 AI-Powered Learning Features

### 📸 Learn from Anything
Upload **any image** — textbook page, street sign, menu, nature photo — and Gemini discovers 4-6 learning opportunities across Physics, History, Math, Art, and more.

### 🎓 Reverse Classroom
Become the teacher! Explain concepts to an AI student who asks clarifying questions, sometimes pretends to be confused, and helps you build deep understanding.

### ⏰ Time Travel Interview
Chat with historical figures — **Gandhi, Einstein, Marie Curie, APJ Abdul Kalam**. They respond in character, in your selected language, with historical accuracy.

### 🔬 Misconception Cascade Tracing (MCT)
When you make a mistake, most apps say "Wrong, here's the answer." That's useless. MCT uses a **5-phase Socratic diagnostic**:

```
Surface Error → Diagnostic Probing → Root Found → Remediation → Verification
```

The AI traces your mistake to the **root misconception**, then repairs it layer by layer.

### 🔗 Concept Collision
Discover surprising connections between topics you've learned. "How is the Pythagorean Theorem connected to music?" — let Gemini blow your mind.

### ⚔️ Debate Arena
Take any position on a topic. Gemini argues the **opposite** using evidence, logic, and fair scoring — building critical thinking skills.

### 📺 YouTube to Course
Paste a video transcript. Gemini generates a structured course with chapters, summaries, quizzes, and learning objectives.

### 🎯 Dream Project Path
Describe your dream project (app, robot, art piece). Gemini creates a personalized learning roadmap with milestones and checkpoints.

---

## 🌍 Multi-Language Support

Fun Learn speaks **9 languages** natively:

| Language | Native Name |
|----------|-------------|
| English | English |
| Hindi | हिन्दी |
| Bengali | বাংলা |
| Spanish | Español |
| Japanese | 日本語 |
| Mandarin | 中文 |
| Arabic | العربية |
| Portuguese | Português |
| French | Français |

**One click** in the header dropdown, and **all AI responses** switch to your language — including historical figure interviews!

---

## 🔊 Voice & Accessibility

- **Text-to-Speech**: Narration powered by Google Cloud TTS
- **Speech-to-Text**: Voice input for answers
- **Full Vocal Mode**: Complete hands-free operation
- **Multi-voice**: Different voices for different characters

---

## 🏆 Gamification

| Feature | Description |
|---------|-------------|
| **XP & Levels** | Earn points for learning activities |
| **Daily Streaks** | Streak bonuses keep you coming back |
| **Teams** | Create and join learning squads |
| **Tournaments** | Compete in timed learning events |
| **Leaderboards** | Global and tournament rankings |

---

## 🎨 Avatar & Characters

- **Create Your Avatar**: Draw, upload, or generate with AI
- **Custom Characters**: Create characters that appear in your stories
- **Multiple Styles**: Cartoon or realistic visual styles
- **Story Integration**: Your characters become part of learning narratives

---

## 🛠️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + TypeScript)            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │LanguageContext│  │ Feature Pages│  │ Chat Components│         │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │ API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI + Python)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Feature Routes│  │Chat Service  │  │Feynman Service│         │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              PROVIDER FACTORY (Plug & Play)              │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │  │
│  │  │ Gemini  │  │ Imagen  │  │ GCP TTS │  │ GCP STT │     │  │
│  │  │   AI    │  │    3    │  │  Voice  │  │  Voice  │     │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Provider Abstraction
Switch between AI providers **without code changes**:

```env
AI_PROVIDER=gemini          # Gemini 3 for AI
IMAGE_PROVIDER=gemini       # Imagen 3 for Images
VOICE_TTS_PROVIDER=gcp      # Google Cloud TTS
VOICE_STT_PROVIDER=gcp      # Google Cloud STT
```

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Tailwind CSS, Vite, Zustand |
| **Backend** | FastAPI, Python 3.11+, Pydantic, httpx (async) |
| **AI** | Gemini 3 Pro Preview (text), Imagen 3 (images) |
| **Voice** | Google Cloud TTS/STT |
| **Data** | CSV files (pandas), local filesystem |
| **Auth** | JWT + bcrypt |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Gemini API Key

### Backend Setup

```bash
cd genlearn-ai/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your API keys

# Start server
python run.py
```

### Frontend Setup

```bash
cd genlearn-ai/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Access the App
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/docs

### Default Login
| Username | Password |
|----------|----------|
| DebK | password123 |

---

## 🔑 Environment Variables

```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Provider Selection
AI_PROVIDER=gemini
IMAGE_PROVIDER=gemini
VOICE_TTS_PROVIDER=gcp
VOICE_STT_PROVIDER=gcp

# Google Cloud (for voice)
GCP_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

---

## � Security Notice

**⚠️ This repository is submitted for the Gemini 3 Hackathon.**

**DO NOT use production API keys from this repository.** All API keys shown are examples only.

**To run this project:**
1. Get your own [Gemini API key](https://ai.google.dev/)
2. Set up your own [Google Cloud project](https://cloud.google.com/) for voice services
3. Copy `.env.example` to `.env` and add your own credentials
4. Never commit your `.env` file or share your real API keys

**Protected files (not included in repository):**
- Production `.env` files with real API keys
- Service account JSON files (`secrets/` folder)
- User data and generated media files
- Deployment scripts with project-specific configurations

---

## �📊 Data Storage

| CSV File | Purpose |
|----------|---------|
| `users.csv` | User accounts and profiles |
| `sessions.csv` | Learning sessions |
| `feynman_sessions.csv` | Feynman Engine sessions |
| `feynman_conversations.csv` | Layer conversations |
| `mct_sessions.csv` | MCT diagnostic sessions |
| `mct_conversations.csv` | MCT chat history |
| `avatars.csv` | User avatars |
| `characters.csv` | Custom characters |
| `tournaments.csv` | Tournament data |
| `teams.csv` | Team information |

---

## 🎬 Demo Script (3 minutes)

1. **[0:00-0:20]** Show the problem: passive learning fails
2. **[0:20-0:45]** Demo Feynman Engine: teach Ritty photosynthesis
3. **[0:45-1:15]** Demo MCT: enter wrong answer, watch AI trace root cause
4. **[1:15-1:45]** Demo Time Travel: interview Marie Curie in Bengali
5. **[1:45-2:15]** Demo Debate Arena: argue about AI replacing teachers
6. **[2:15-2:45]** Flash architecture: 100% Gemini-powered
7. **[2:45-3:00]** Close: "Education shouldn't be passive. With Gemini, it finally isn't."

---

## 🏗️ Project Structure

```
genlearn-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # API endpoints
│   │   ├── services/         # Business logic + AI providers
│   │   ├── database/         # CSV handlers
│   │   └── utils/            # Helpers + language support
│   ├── data/
│   │   ├── csv/              # Database files
│   │   └── media/            # Generated images
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/       # Reusable UI components
    │   ├── contexts/         # React contexts (Language, Auth)
    │   ├── pages/            # Feature pages
    │   ├── services/         # API client
    │   └── utils/            # Helpers
    └── package.json
```

---

## 🙏 Acknowledgments

Built with ❤️ using:
- [Google Gemini](https://deepmind.google/technologies/gemini/) - AI backbone
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Google Cloud Platform](https://cloud.google.com/) - Voice services

---

<div align="center">

**Made for Google Gemini 3 Hackathon 2026**

*Fun Learn — Where understanding happens by teaching, not by being taught.*

</div>
