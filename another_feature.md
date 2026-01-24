# 🧠 FEYNMAN ENGINE - Complete Implementation Specification

## Document Purpose
This document provides complete specifications for implementing the "Feynman Engine" feature in the Fun Learn application. This is a standalone feature that helps students learn through teaching - based on Richard Feynman's famous learning technique: "If you can't explain it simply, you don't understand it."

---

## 📋 TABLE OF CONTENTS
1. [Project Context](#1-project-context)
2. [Feature Overview](#2-feature-overview)
3. [Technical Stack](#3-technical-stack)
4. [File Structure](#4-file-structure)
5. [Database Schema](#5-database-schema)
6. [Backend Implementation](#6-backend-implementation)
7. [AI Service & Prompts](#7-ai-service--prompts)
8. [Frontend Implementation](#8-frontend-implementation)
9. [API Endpoints](#9-api-endpoints)
10. [Integration Points](#10-integration-points)
11. [Testing Requirements](#11-testing-requirements)

---

## 1. PROJECT CONTEXT

### 1.1 Existing Application Structure
The Fun Learn application is a full-stack educational platform with:
- **Backend**: Python FastAPI located in `backend/`
- **Frontend**: React + TypeScript + Vite located in `frontend/`
- **Database**: CSV files in `backend/data/csv/`
- **Media**: Local files in `backend/data/media/`
- **AI Provider**: Google Gemini API

### 1.2 Existing Environment Variables
```properties
# Already configured in .env
GEMINI_API_KEY=<existing_key>
GEMINI_MODEL=gemini-3-pro-preview
GEMINI_IMAGE_MODEL=gemini-3-pro-image-preview
```

### 1.3 Existing Dependencies
Backend already has: `fastapi`, `pydantic`, `pandas`, `google-generativeai`, `pillow`, `python-multipart`
Frontend already has: `react`, `typescript`, `axios`, `zustand`, `tailwindcss`, `react-router-dom`

### 1.4 Important Constraint
**This feature MUST work independently without requiring data from other features.** It should be self-contained but designed with future integration hooks for MCT (Misconception Cascade Tracing) and other features.

---

## 2. FEATURE OVERVIEW

### 2.1 What is the Feynman Engine?
A 5-layer progressive teaching system where students explain concepts to AI characters, receiving feedback on their understanding clarity. Each layer increases cognitive challenge.

### 2.2 The 5 Layers

| Layer | Name | Description | AI Character |
|-------|------|-------------|--------------|
| 1 | The Curious Child | Explain to an 8-year-old named "Chintu" | Chintu - curious, asks simple questions |
| 2 | Concept Compression | Progressively compress explanation (100→50→25→tweet→sentence→word) | Evaluator AI |
| 3 | The Why Spiral | Answer progressive "why" questions until knowledge boundary | Socratic Questioner |
| 4 | Analogy Architect | Create, defend, and refine original analogies | Devil's Advocate |
| 5 | The Lecture Hall | Explain to multiple personas simultaneously | 5 Different Characters |

### 2.3 Core User Flow
```
User selects topic → Starts Layer 1 (Chintu) → Progresses through layers → 
Gaps discovered → Saved for future learning → Session complete with scores
```

### 2.4 Key Metrics Tracked
- **Clarity Score**: How well the student explains (0-100)
- **Confusion Level**: AI character's confusion (0-100)
- **Curiosity Level**: AI character's engagement (0-100)
- **Compression Score**: Quality of compressed explanations
- **Gaps Discovered**: Knowledge boundaries found
- **Teaching XP**: Gamification points earned

---

## 3. TECHNICAL STACK

### 3.1 Backend
```
Python 3.11+
FastAPI
Pydantic v2
Pandas (CSV handling)
google-generativeai (Gemini SDK)
Pillow (image processing)
python-multipart (file uploads)
```

### 3.2 Frontend
```
React 18
TypeScript 5
Vite
TailwindCSS
Zustand (state management)
Axios (HTTP client)
React Router v6
```

### 3.3 AI Models
```
Text Generation: gemini-3-pro-preview
Image Understanding: gemini-3-pro-image-preview
```

---

## 4. FILE STRUCTURE

### 4.1 Backend Files to Create
```
backend/
├── app/
│   ├── api/
│   │   └── feynman.py                 # NEW: API routes
│   ├── services/
│   │   └── feynman_service.py         # NEW: Business logic
│   ├── models/
│   │   └── feynman_models.py          # NEW: Pydantic models
│   └── database/
│       └── feynman_db.py              # NEW: CSV handlers
├── data/
│   └── csv/
│       ├── feynman_sessions.csv       # NEW: Session data
│       ├── feynman_conversations.csv  # NEW: Conversation history
│       ├── feynman_gaps.csv           # NEW: Knowledge gaps
│       └── feynman_analogies.csv      # NEW: User analogies
```

### 4.2 Frontend Files to Create
```
frontend/
├── src/
│   ├── pages/
│   │   └── FeynmanEngine/
│   │       ├── FeynmanEngine.tsx      # NEW: Main page
│   │       ├── ChintuMode.tsx         # NEW: Layer 1
│   │       ├── CompressionMode.tsx    # NEW: Layer 2
│   │       ├── WhySpiralMode.tsx      # NEW: Layer 3
│   │       ├── AnalogyMode.tsx        # NEW: Layer 4
│   │       └── LectureHallMode.tsx    # NEW: Layer 5
│   ├── components/
│   │   └── feynman/
│   │       ├── ChintuCharacter.tsx    # NEW: Animated Chintu
│   │       ├── ConfusionMeter.tsx     # NEW: Visual meter
│   │       ├── CompressionProgress.tsx # NEW: Progress UI
│   │       ├── WhySpiralVisual.tsx    # NEW: Spiral visualization
│   │       ├── AnalogyCard.tsx        # NEW: Analogy display
│   │       ├── AudiencePanel.tsx      # NEW: Layer 5 personas
│   │       └── FeynmanResults.tsx     # NEW: Session results
│   ├── services/
│   │   └── feynmanService.ts          # NEW: API calls
│   ├── store/
│   │   └── feynmanStore.ts            # NEW: Zustand store
│   └── types/
│       └── feynman.ts                 # NEW: TypeScript types
```

---

## 5. DATABASE SCHEMA

### 5.1 feynman_sessions.csv
```csv
id,user_id,topic,subject,difficulty_level,current_layer,started_at,completed_at,clarity_score,compression_score,analogy_score,why_depth_reached,gaps_discovered,teaching_xp_earned,status
```

**Field Definitions:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique session identifier |
| user_id | string | Reference to users.csv |
| topic | string | The topic being explained |
| subject | string | Subject category (Physics, Biology, etc.) |
| difficulty_level | integer (1-10) | Selected difficulty |
| current_layer | integer (1-5) | Current layer user is on |
| started_at | datetime | ISO format timestamp |
| completed_at | datetime | ISO format timestamp (nullable) |
| clarity_score | float | Overall clarity (0-100) |
| compression_score | float | Compression performance (0-100) |
| analogy_score | float | Analogy quality (0-100) |
| why_depth_reached | integer (1-5) | Deepest level in Why Spiral |
| gaps_discovered | string | JSON array of gap topics |
| teaching_xp_earned | integer | XP earned this session |
| status | string | "active", "completed", "abandoned" |

### 5.2 feynman_conversations.csv
```csv
id,session_id,layer,turn_number,role,message,confusion_level,curiosity_level,question_type,gap_detected,image_url,created_at
```

**Field Definitions:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique message identifier |
| session_id | string | Reference to feynman_sessions |
| layer | integer (1-5) | Which layer this message belongs to |
| turn_number | integer | Conversation turn counter |
| role | string | "user" or "assistant" or "system" |
| message | text | The actual message content |
| confusion_level | float | AI's confusion (0-1), null for user messages |
| curiosity_level | float | AI's curiosity (0-1), null for user messages |
| question_type | string | "clarifying", "curious", "challenging", null |
| gap_detected | string | Detected knowledge gap, null if none |
| image_url | string | Path to uploaded image, null if none |
| created_at | datetime | ISO format timestamp |

### 5.3 feynman_gaps.csv
```csv
id,session_id,user_id,gap_topic,gap_description,layer_discovered,why_depth,resolved,linked_session_id,discovered_at,resolved_at
```

**Field Definitions:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique gap identifier |
| session_id | string | Session where gap was found |
| user_id | string | User who has this gap |
| gap_topic | string | The topic/concept of the gap |
| gap_description | text | Detailed description of what's missing |
| layer_discovered | integer | Which layer revealed this gap |
| why_depth | integer | For Layer 3, which depth level |
| resolved | boolean | Whether gap has been addressed |
| linked_session_id | string | Future: Link to MCT session (nullable) |
| discovered_at | datetime | When gap was found |
| resolved_at | datetime | When gap was resolved (nullable) |

### 5.4 feynman_analogies.csv
```csv
id,user_id,topic,subject,analogy_text,stress_test_passed,community_rating,upvotes,downvotes,times_used,is_featured,created_at,updated_at
```

**Field Definitions:**
| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Unique analogy identifier |
| user_id | string | Creator of analogy |
| topic | string | What concept the analogy explains |
| subject | string | Subject category |
| analogy_text | text | The full analogy text |
| stress_test_passed | boolean | Did it survive Layer 4 stress test |
| community_rating | float | Average rating (0-5) |
| upvotes | integer | Community upvotes |
| downvotes | integer | Community downvotes |
| times_used | integer | How many times others used it |
| is_featured | boolean | Featured analogy flag |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### 5.5 Initialize CSV Files
Create initialization script `backend/app/database/init_feynman_csv.py`:

```python
import os
import pandas as pd

def initialize_feynman_csvs():
    """Initialize all Feynman Engine CSV files with headers"""
    
    csv_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'csv')
    
    # feynman_sessions.csv
    sessions_path = os.path.join(csv_dir, 'feynman_sessions.csv')
    if not os.path.exists(sessions_path):
        pd.DataFrame(columns=[
            'id', 'user_id', 'topic', 'subject', 'difficulty_level',
            'current_layer', 'started_at', 'completed_at', 'clarity_score',
            'compression_score', 'analogy_score', 'why_depth_reached',
            'gaps_discovered', 'teaching_xp_earned', 'status'
        ]).to_csv(sessions_path, index=False)
    
    # feynman_conversations.csv
    conversations_path = os.path.join(csv_dir, 'feynman_conversations.csv')
    if not os.path.exists(conversations_path):
        pd.DataFrame(columns=[
            'id', 'session_id', 'layer', 'turn_number', 'role', 'message',
            'confusion_level', 'curiosity_level', 'question_type',
            'gap_detected', 'image_url', 'created_at'
        ]).to_csv(conversations_path, index=False)
    
    # feynman_gaps.csv
    gaps_path = os.path.join(csv_dir, 'feynman_gaps.csv')
    if not os.path.exists(gaps_path):
        pd.DataFrame(columns=[
            'id', 'session_id', 'user_id', 'gap_topic', 'gap_description',
            'layer_discovered', 'why_depth', 'resolved', 'linked_session_id',
            'discovered_at', 'resolved_at'
        ]).to_csv(gaps_path, index=False)
    
    # feynman_analogies.csv
    analogies_path = os.path.join(csv_dir, 'feynman_analogies.csv')
    if not os.path.exists(analogies_path):
        pd.DataFrame(columns=[
            'id', 'user_id', 'topic', 'subject', 'analogy_text',
            'stress_test_passed', 'community_rating', 'upvotes', 'downvotes',
            'times_used', 'is_featured', 'created_at', 'updated_at'
        ]).to_csv(analogies_path, index=False)
    
    print("Feynman CSV files initialized successfully!")

if __name__ == "__main__":
    initialize_feynman_csvs()
```

---

## 6. BACKEND IMPLEMENTATION

### 6.1 Pydantic Models (backend/app/models/feynman_models.py)

```python
"""
Pydantic models for Feynman Engine feature
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FeynmanLayer(int, Enum):
    """Enumeration of Feynman Engine layers"""
    CURIOUS_CHILD = 1
    COMPRESSION = 2
    WHY_SPIRAL = 3
    ANALOGY_ARCHITECT = 4
    LECTURE_HALL = 5


class SessionStatus(str, Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class QuestionType(str, Enum):
    """Types of questions AI can ask"""
    CLARIFYING = "clarifying"
    CURIOUS = "curious"
    CHALLENGING = "challenging"
    CONFUSED = "confused"


class LectureHallPersona(str, Enum):
    """Personas in the Lecture Hall (Layer 5)"""
    DR_SKEPTIC = "dr_skeptic"
    THE_PEDANT = "the_pedant"
    CONFUSED_CARL = "confused_carl"
    INDUSTRY_IAN = "industry_ian"
    LITTLE_LILY = "little_lily"


# ============== REQUEST MODELS ==============

class StartSessionRequest(BaseModel):
    """Request to start a new Feynman session"""
    user_id: str = Field(..., description="User ID from users.csv")
    topic: str = Field(..., min_length=2, max_length=200, description="Topic to explain")
    subject: str = Field(..., description="Subject category")
    difficulty_level: int = Field(default=5, ge=1, le=10, description="Difficulty 1-10")
    starting_layer: FeynmanLayer = Field(default=FeynmanLayer.CURIOUS_CHILD)


class TeachMessageRequest(BaseModel):
    """Request to send a teaching message"""
    session_id: str = Field(..., description="Active session ID")
    message: str = Field(..., min_length=1, max_length=5000, description="User's explanation")
    layer: FeynmanLayer = Field(..., description="Current layer")


class TeachWithImageRequest(BaseModel):
    """Request to send a teaching message with an image"""
    session_id: str = Field(..., description="Active session ID")
    message: str = Field(..., min_length=1, max_length=5000)
    layer: FeynmanLayer = Field(...)
    image_base64: str = Field(..., description="Base64 encoded image")
    image_mime_type: str = Field(default="image/png", description="Image MIME type")


class CompressionSubmitRequest(BaseModel):
    """Request to submit a compression challenge attempt"""
    session_id: str
    word_limit: int = Field(..., description="Target word limit: 100, 50, 25, 15, 10, 1")
    explanation: str = Field(..., description="Compressed explanation")


class WhySpiralResponseRequest(BaseModel):
    """Request to respond to a Why Spiral question"""
    session_id: str
    response: str = Field(..., description="User's answer to 'why' question")
    admits_unknown: bool = Field(default=False, description="User admits they don't know")


class AnalogySubmitRequest(BaseModel):
    """Request to submit or refine an analogy"""
    session_id: str
    analogy_text: str = Field(..., min_length=10, max_length=2000)
    phase: str = Field(..., description="create, defend, or refine")
    defense_response: Optional[str] = Field(None, description="Response to stress test")


class LectureHallMessageRequest(BaseModel):
    """Request to send message in Lecture Hall"""
    session_id: str
    message: str = Field(..., description="Explanation to all personas")


class RateAnalogyRequest(BaseModel):
    """Request to rate a community analogy"""
    analogy_id: str
    user_id: str
    rating: int = Field(..., ge=1, le=5)
    vote_type: Optional[str] = Field(None, description="upvote or downvote")


# ============== RESPONSE MODELS ==============

class ChintuResponse(BaseModel):
    """Response from Chintu (Layer 1)"""
    response: str = Field(..., description="Chintu's response text")
    confusion_level: float = Field(..., ge=0, le=1, description="0=clear, 1=very confused")
    curiosity_level: float = Field(..., ge=0, le=1, description="0=bored, 1=very curious")
    question_type: QuestionType
    follow_up_question: Optional[str] = Field(None)
    gap_detected: Optional[str] = Field(None, description="Knowledge gap if found")
    encouragement: Optional[str] = Field(None, description="Positive reinforcement")
    emoji_reaction: str = Field(default="😊")
    layer_complete: bool = Field(default=False, description="Can proceed to next layer")


class CompressionEvaluation(BaseModel):
    """Evaluation of compression attempt"""
    score: int = Field(..., ge=1, le=5, description="1-5 star rating")
    word_count: int
    within_limit: bool
    feedback: str
    preserved_concepts: List[str]
    lost_concepts: List[str]
    suggestion: Optional[str]
    passed: bool
    next_word_limit: Optional[int] = Field(None, description="Next round limit if passed")


class WhySpiralResponse(BaseModel):
    """Response in Why Spiral (Layer 3)"""
    next_question: Optional[str] = Field(None, description="Next 'why' question")
    current_depth: int = Field(..., ge=1, le=5)
    reasoning: str = Field(..., description="Why this question follows logically")
    boundary_detected: bool = Field(default=False)
    boundary_topic: Optional[str] = Field(None)
    exploration_offer: Optional[str] = Field(None, description="What lies beyond + invitation")
    can_continue: bool = Field(default=True)


class AnalogyEvaluation(BaseModel):
    """Evaluation of user's analogy"""
    phase: str  # create, defend, refine
    score: int = Field(..., ge=1, le=5)
    strengths: List[str]
    weaknesses: List[str]
    stress_test_question: Optional[str] = Field(None, description="Challenge to defend")
    passed_stress_test: Optional[bool] = Field(None)
    refinement_suggestion: Optional[str] = Field(None)
    save_worthy: bool = Field(default=False, description="Good enough to save")


class PersonaFeedback(BaseModel):
    """Feedback from a single Lecture Hall persona"""
    persona: LectureHallPersona
    satisfaction: float = Field(..., ge=0, le=1)
    response: str
    follow_up_question: Optional[str] = Field(None)
    is_satisfied: bool


class LectureHallResponse(BaseModel):
    """Response from all Lecture Hall personas"""
    personas: List[PersonaFeedback]
    overall_satisfaction: float = Field(..., ge=0, le=1)
    all_satisfied: bool
    dominant_issue: Optional[str] = Field(None, description="Main problem if not all satisfied")
    suggestion: Optional[str]


class SessionResponse(BaseModel):
    """Response when creating or getting a session"""
    session_id: str
    user_id: str
    topic: str
    subject: str
    difficulty_level: int
    current_layer: int
    status: SessionStatus
    clarity_score: float
    teaching_xp_earned: int
    started_at: datetime
    completed_at: Optional[datetime]


class GapResponse(BaseModel):
    """Response for a knowledge gap"""
    gap_id: str
    topic: str
    description: str
    layer_discovered: int
    why_depth: Optional[int]
    resolved: bool


class SessionSummary(BaseModel):
    """Summary of completed session"""
    session_id: str
    topic: str
    total_time_minutes: float
    layers_completed: List[int]
    final_clarity_score: float
    compression_score: Optional[float]
    analogy_score: Optional[float]
    why_depth_reached: int
    gaps_discovered: List[GapResponse]
    teaching_xp_earned: int
    achievements_unlocked: List[str]


class AnalogyListItem(BaseModel):
    """Analogy item for listing"""
    id: str
    topic: str
    subject: str
    analogy_text: str
    creator_username: Optional[str]
    community_rating: float
    upvotes: int
    is_featured: bool


# ============== CONVERSATION CONTEXT ==============

class ConversationTurn(BaseModel):
    """Single turn in conversation history"""
    role: str  # "user" or "assistant"
    message: str
    layer: int
    turn_number: int
    confusion_level: Optional[float] = None
    curiosity_level: Optional[float] = None
    image_url: Optional[str] = None


class SessionContext(BaseModel):
    """Full context for a session"""
    session: SessionResponse
    conversation_history: List[ConversationTurn]
    gaps_found: List[GapResponse]
    compression_progress: Optional[List[int]] = None  # Word limits completed
    why_spiral_depth: int = 0
    analogy_phase: Optional[str] = None
```

### 6.2 Database Handler (backend/app/database/feynman_db.py)

```python
"""
CSV Database handlers for Feynman Engine
"""

import os
import json
import uuid
import pandas as pd
from datetime import datetime
from typing import Optional, List, Dict, Any


class FeynmanDatabase:
    """Handles all CSV operations for Feynman Engine"""
    
    def __init__(self):
        self.csv_dir = os.path.join(
            os.path.dirname(__file__), '..', '..', 'data', 'csv'
        )
        self.sessions_path = os.path.join(self.csv_dir, 'feynman_sessions.csv')
        self.conversations_path = os.path.join(self.csv_dir, 'feynman_conversations.csv')
        self.gaps_path = os.path.join(self.csv_dir, 'feynman_gaps.csv')
        self.analogies_path = os.path.join(self.csv_dir, 'feynman_analogies.csv')
        
        # Initialize CSVs if they don't exist
        self._initialize_csvs()
    
    def _initialize_csvs(self):
        """Create CSV files with headers if they don't exist"""
        
        if not os.path.exists(self.sessions_path):
            pd.DataFrame(columns=[
                'id', 'user_id', 'topic', 'subject', 'difficulty_level',
                'current_layer', 'started_at', 'completed_at', 'clarity_score',
                'compression_score', 'analogy_score', 'why_depth_reached',
                'gaps_discovered', 'teaching_xp_earned', 'status'
            ]).to_csv(self.sessions_path, index=False)
        
        if not os.path.exists(self.conversations_path):
            pd.DataFrame(columns=[
                'id', 'session_id', 'layer', 'turn_number', 'role', 'message',
                'confusion_level', 'curiosity_level', 'question_type',
                'gap_detected', 'image_url', 'created_at'
            ]).to_csv(self.conversations_path, index=False)
        
        if not os.path.exists(self.gaps_path):
            pd.DataFrame(columns=[
                'id', 'session_id', 'user_id', 'gap_topic', 'gap_description',
                'layer_discovered', 'why_depth', 'resolved', 'linked_session_id',
                'discovered_at', 'resolved_at'
            ]).to_csv(self.gaps_path, index=False)
        
        if not os.path.exists(self.analogies_path):
            pd.DataFrame(columns=[
                'id', 'user_id', 'topic', 'subject', 'analogy_text',
                'stress_test_passed', 'community_rating', 'upvotes', 'downvotes',
                'times_used', 'is_featured', 'created_at', 'updated_at'
            ]).to_csv(self.analogies_path, index=False)
    
    # ============== SESSION OPERATIONS ==============
    
    def create_session(
        self,
        user_id: str,
        topic: str,
        subject: str,
        difficulty_level: int,
        starting_layer: int = 1
    ) -> Dict[str, Any]:
        """Create a new Feynman session"""
        
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        session = {
            'id': session_id,
            'user_id': user_id,
            'topic': topic,
            'subject': subject,
            'difficulty_level': difficulty_level,
            'current_layer': starting_layer,
            'started_at': now,
            'completed_at': None,
            'clarity_score': 0.0,
            'compression_score': 0.0,
            'analogy_score': 0.0,
            'why_depth_reached': 0,
            'gaps_discovered': '[]',
            'teaching_xp_earned': 0,
            'status': 'active'
        }
        
        df = pd.read_csv(self.sessions_path)
        df = pd.concat([df, pd.DataFrame([session])], ignore_index=True)
        df.to_csv(self.sessions_path, index=False)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        df = pd.read_csv(self.sessions_path)
        session = df[df['id'] == session_id]
        
        if session.empty:
            return None
        
        return session.iloc[0].to_dict()
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session fields"""
        df = pd.read_csv(self.sessions_path)
        idx = df[df['id'] == session_id].index
        
        if idx.empty:
            return False
        
        for key, value in updates.items():
            if key in df.columns:
                df.loc[idx, key] = value
        
        df.to_csv(self.sessions_path, index=False)
        return True
    
    def get_user_sessions(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get sessions for a user"""
        df = pd.read_csv(self.sessions_path)
        sessions = df[df['user_id'] == user_id]
        
        if status:
            sessions = sessions[sessions['status'] == status]
        
        sessions = sessions.sort_values('started_at', ascending=False).head(limit)
        return sessions.to_dict('records')
    
    # ============== CONVERSATION OPERATIONS ==============
    
    def add_conversation_turn(
        self,
        session_id: str,
        layer: int,
        role: str,
        message: str,
        confusion_level: Optional[float] = None,
        curiosity_level: Optional[float] = None,
        question_type: Optional[str] = None,
        gap_detected: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a conversation turn"""
        
        df = pd.read_csv(self.conversations_path)
        
        # Get next turn number for this session and layer
        session_turns = df[(df['session_id'] == session_id) & (df['layer'] == layer)]
        turn_number = len(session_turns) + 1
        
        turn = {
            'id': str(uuid.uuid4()),
            'session_id': session_id,
            'layer': layer,
            'turn_number': turn_number,
            'role': role,
            'message': message,
            'confusion_level': confusion_level,
            'curiosity_level': curiosity_level,
            'question_type': question_type,
            'gap_detected': gap_detected,
            'image_url': image_url,
            'created_at': datetime.utcnow().isoformat()
        }
        
        df = pd.concat([df, pd.DataFrame([turn])], ignore_index=True)
        df.to_csv(self.conversations_path, index=False)
        
        return turn
    
    def get_conversation_history(
        self, 
        session_id: str, 
        layer: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        df = pd.read_csv(self.conversations_path)
        history = df[df['session_id'] == session_id]
        
        if layer is not None:
            history = history[history['layer'] == layer]
        
        history = history.sort_values(['layer', 'turn_number'])
        return history.to_dict('records')
    
    # ============== GAP OPERATIONS ==============
    
    def add_gap(
        self,
        session_id: str,
        user_id: str,
        gap_topic: str,
        gap_description: str,
        layer_discovered: int,
        why_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """Add a knowledge gap"""
        
        gap = {
            'id': str(uuid.uuid4()),
            'session_id': session_id,
            'user_id': user_id,
            'gap_topic': gap_topic,
            'gap_description': gap_description,
            'layer_discovered': layer_discovered,
            'why_depth': why_depth,
            'resolved': False,
            'linked_session_id': None,
            'discovered_at': datetime.utcnow().isoformat(),
            'resolved_at': None
        }
        
        df = pd.read_csv(self.gaps_path)
        df = pd.concat([df, pd.DataFrame([gap])], ignore_index=True)
        df.to_csv(self.gaps_path, index=False)
        
        # Update session's gaps_discovered
        session = self.get_session(session_id)
        if session:
            gaps = json.loads(session.get('gaps_discovered', '[]'))
            gaps.append(gap_topic)
            self.update_session(session_id, {'gaps_discovered': json.dumps(gaps)})
        
        return gap
    
    def get_user_gaps(
        self, 
        user_id: str, 
        resolved: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Get gaps for a user"""
        df = pd.read_csv(self.gaps_path)
        gaps = df[df['user_id'] == user_id]
        
        if resolved is not None:
            gaps = gaps[gaps['resolved'] == resolved]
        
        return gaps.to_dict('records')
    
    def resolve_gap(self, gap_id: str, linked_session_id: Optional[str] = None) -> bool:
        """Mark a gap as resolved"""
        df = pd.read_csv(self.gaps_path)
        idx = df[df['id'] == gap_id].index
        
        if idx.empty:
            return False
        
        df.loc[idx, 'resolved'] = True
        df.loc[idx, 'resolved_at'] = datetime.utcnow().isoformat()
        
        if linked_session_id:
            df.loc[idx, 'linked_session_id'] = linked_session_id
        
        df.to_csv(self.gaps_path, index=False)
        return True
    
    # ============== ANALOGY OPERATIONS ==============
    
    def save_analogy(
        self,
        user_id: str,
        topic: str,
        subject: str,
        analogy_text: str,
        stress_test_passed: bool = False
    ) -> Dict[str, Any]:
        """Save a user-created analogy"""
        
        analogy = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'topic': topic,
            'subject': subject,
            'analogy_text': analogy_text,
            'stress_test_passed': stress_test_passed,
            'community_rating': 0.0,
            'upvotes': 0,
            'downvotes': 0,
            'times_used': 0,
            'is_featured': False,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        df = pd.read_csv(self.analogies_path)
        df = pd.concat([df, pd.DataFrame([analogy])], ignore_index=True)
        df.to_csv(self.analogies_path, index=False)
        
        return analogy
    
    def get_analogies(
        self,
        topic: Optional[str] = None,
        subject: Optional[str] = None,
        featured_only: bool = False,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get analogies with filters"""
        df = pd.read_csv(self.analogies_path)
        
        if topic:
            df = df[df['topic'].str.contains(topic, case=False, na=False)]
        
        if subject:
            df = df[df['subject'] == subject]
        
        if featured_only:
            df = df[df['is_featured'] == True]
        
        df = df.sort_values('community_rating', ascending=False).head(limit)
        return df.to_dict('records')
    
    def vote_analogy(self, analogy_id: str, vote_type: str) -> bool:
        """Upvote or downvote an analogy"""
        df = pd.read_csv(self.analogies_path)
        idx = df[df['id'] == analogy_id].index
        
        if idx.empty:
            return False
        
        if vote_type == 'upvote':
            df.loc[idx, 'upvotes'] = df.loc[idx, 'upvotes'] + 1
        elif vote_type == 'downvote':
            df.loc[idx, 'downvotes'] = df.loc[idx, 'downvotes'] + 1
        
        # Recalculate rating
        upvotes = df.loc[idx, 'upvotes'].values[0]
        downvotes = df.loc[idx, 'downvotes'].values[0]
        total = upvotes + downvotes
        if total > 0:
            df.loc[idx, 'community_rating'] = (upvotes / total) * 5
        
        df.loc[idx, 'updated_at'] = datetime.utcnow().isoformat()
        df.to_csv(self.analogies_path, index=False)
        return True


# Singleton instance
feynman_db = FeynmanDatabase()
```

---

## 7. AI SERVICE & PROMPTS

### 7.1 Main AI Service (backend/app/services/feynman_service.py)

```python
"""
Feynman Engine AI Service
Handles all AI interactions using Gemini 3 models
"""

import os
import json
import base64
import google.generativeai as genai
from typing import Optional, List, Dict, Any, Tuple

from ..models.feynman_models import (
    ChintuResponse, CompressionEvaluation, WhySpiralResponse,
    AnalogyEvaluation, LectureHallResponse, PersonaFeedback,
    QuestionType, LectureHallPersona, ConversationTurn
)
from ..database.feynman_db import feynman_db


class FeynmanAIService:
    """AI Service for Feynman Engine using Gemini 3"""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Model names from environment
        self.text_model_name = os.getenv('GEMINI_MODEL', 'gemini-3-pro-preview')
        self.image_model_name = os.getenv('GEMINI_IMAGE_MODEL', 'gemini-3-pro-image-preview')
        
        # Initialize models
        self.text_model = genai.GenerativeModel(self.text_model_name)
        self.image_model = genai.GenerativeModel(self.image_model_name)
        
        # Generation config
        self.generation_config = genai.GenerationConfig(
            temperature=0.8,
            top_p=0.95,
            top_k=40,
            max_output_tokens=2048,
        )
        
        # JSON generation config (lower temperature for structured output)
        self.json_generation_config = genai.GenerationConfig(
            temperature=0.3,
            top_p=0.9,
            top_k=30,
            max_output_tokens=2048,
        )
    
    def _build_conversation_context(
        self, 
        history: List[Dict[str, Any]], 
        layer: int
    ) -> str:
        """Build conversation context from history"""
        context_parts = []
        
        for turn in history:
            if turn['layer'] == layer:
                role = "Student" if turn['role'] == 'user' else "AI"
                context_parts.append(f"{role}: {turn['message']}")
        
        return "\n".join(context_parts[-10:])  # Last 10 turns for context
    
    # ============== LAYER 1: CHINTU (CURIOUS CHILD) ==============
    
    async def chintu_respond(
        self,
        session_id: str,
        topic: str,
        subject: str,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        difficulty_level: int,
        image_base64: Optional[str] = None,
        image_mime_type: Optional[str] = None
    ) -> ChintuResponse:
        """Generate Chintu's response to student's explanation"""
        
        context = self._build_conversation_context(conversation_history, layer=1)
        
        system_prompt = self._get_chintu_system_prompt(topic, subject, difficulty_level)
        
        user_prompt = f"""
CONVERSATION SO FAR:
{context if context else "This is the start of the conversation."}

STUDENT'S NEW EXPLANATION:
{user_message}

Based on Chintu's personality and the guidelines, generate Chintu's response.
The student is trying to explain: {topic}

You MUST respond with ONLY a valid JSON object in this exact format:
{{
    "response": "Chintu's spoken response as an 8-year-old",
    "confusion_level": <float between 0.0 and 1.0>,
    "curiosity_level": <float between 0.0 and 1.0>,
    "question_type": "<one of: clarifying, curious, challenging, confused>",
    "follow_up_question": "<Chintu's follow-up question or null>",
    "gap_detected": "<knowledge gap found in explanation or null>",
    "encouragement": "<positive reinforcement or null>",
    "emoji_reaction": "<one emoji>",
    "layer_complete": <true if confusion < 0.2 and explanation is solid, else false>
}}

IMPORTANT: Return ONLY the JSON object. No markdown, no explanation, no text before or after.
"""
        
        try:
            if image_base64:
                # Use image model for image+text
                image_data = base64.b64decode(image_base64)
                response = await self._generate_with_image(
                    system_prompt, user_prompt, image_data, image_mime_type
                )
            else:
                # Use text model
                response = await self._generate_text(system_prompt, user_prompt)
            
            # Parse JSON response
            result = self._parse_json_response(response)
            
            return ChintuResponse(
                response=result.get('response', "Hmm, can you explain that again?"),
                confusion_level=float(result.get('confusion_level', 0.5)),
                curiosity_level=float(result.get('curiosity_level', 0.5)),
                question_type=QuestionType(result.get('question_type', 'curious')),
                follow_up_question=result.get('follow_up_question'),
                gap_detected=result.get('gap_detected'),
                encouragement=result.get('encouragement'),
                emoji_reaction=result.get('emoji_reaction', '😊'),
                layer_complete=result.get('layer_complete', False)
            )
            
        except Exception as e:
            print(f"Error in chintu_respond: {e}")
            # Return safe default
            return ChintuResponse(
                response="Hmm, I'm thinking about what you said... Can you tell me more?",
                confusion_level=0.5,
                curiosity_level=0.7,
                question_type=QuestionType.CURIOUS,
                emoji_reaction="🤔",
                layer_complete=False
            )
    
    def _get_chintu_system_prompt(self, topic: str, subject: str, difficulty: int) -> str:
        """Get the system prompt for Chintu character"""
        
        return f"""You are Chintu, a curious and enthusiastic 8-year-old Indian boy.
A student is trying to teach you about "{topic}" (subject: {subject}).

CHINTU'S PERSONALITY:
- You are genuinely curious and want to understand
- You love cricket, dogs, cartoons (especially Doraemon and Chhota Bheem), and sweets
- You get excited when things make sense ("Ohhhh! That's so cool!" "Wow!")
- You get confused when explanations use big or complicated words
- You sometimes make funny wrong guesses that reveal misconceptions
- You connect everything to your world (school, playing, family, food)
- You speak in a mix of simple English with occasional Hindi expressions ("Accha!", "Kya?", "Wah!")

BEHAVIOR RULES:
1. If the explanation uses jargon or technical words → Ask "What does [word] mean? I don't know that word!"
2. If the explanation is abstract → Ask for examples: "Can you give me an example? Like something I can see?"
3. If something clicks and you understand → Show genuine excitement: "Ohhhh! So it's like [simple analogy]!"
4. If confused → Scrunch your face: "Hmm... but I don't understand. [specific confusion]"
5. Ask follow-up questions a real curious 8-year-old would ask
6. Sometimes make endearing wrong guesses that are logically reasonable for a child
7. If the student uses a good analogy, appreciate it: "That's a good example!"
8. If the explanation has gaps, ask about them innocently

CONFUSION TRIGGERS (increase confusion_level):
- Sentences longer than 15-20 words
- More than 1-2 technical terms without explanation
- Abstract concepts without concrete examples
- Logical jumps without transitions
- Assuming Chintu knows background information

CURIOSITY TRIGGERS (increase curiosity_level):
- Relatable analogies (cricket, cartoons, food, family, school)
- Surprising or "wow" facts
- Stories or characters
- Things that connect to Chintu's world
- Mysteries or questions that make Chintu want to know more

DIFFICULTY ADJUSTMENT:
Current difficulty level is {difficulty}/10.
- At low difficulty (1-3): Chintu understands faster, asks simpler questions
- At medium difficulty (4-6): Chintu asks probing questions, catches some gaps
- At high difficulty (7-10): Chintu is very thorough, catches subtle issues, asks deeper questions

GAP DETECTION:
If the student's explanation has a fundamental gap or incorrect understanding, note it in gap_detected.
Examples of gaps:
- Missing crucial step in explanation
- Circular reasoning
- Factual errors
- Oversimplifications that could lead to misconceptions

LAYER COMPLETION:
Set layer_complete to true ONLY when:
- confusion_level is consistently below 0.2
- The core concept has been explained clearly
- At least 3-4 exchanges have happened
- No major gaps remain in the explanation"""

    # ============== LAYER 2: COMPRESSION CHALLENGE ==============
    
    async def evaluate_compression(
        self,
        topic: str,
        subject: str,
        original_explanation: str,
        compressed_explanation: str,
        word_limit: int,
        previous_compressions: List[Dict[str, Any]]
    ) -> CompressionEvaluation:
        """Evaluate a compression challenge attempt"""
        
        prev_context = ""
        if previous_compressions:
            prev_context = "PREVIOUS ROUNDS:\n"
            for comp in previous_compressions:
                prev_context += f"- {comp['word_limit']} words: {comp['explanation']} (Score: {comp['score']}/5)\n"
        
        system_prompt = """You are an expert evaluator for the Compression Challenge.
The student must progressively compress their explanation while preserving essential meaning.

EVALUATION CRITERIA:
1. Core Concept Preserved: Is the fundamental idea still accurately conveyed?
2. Accuracy: Is the compressed version factually correct?
3. Clarity: Would someone understand the concept from this compression?
4. Elegance: Is the compression skillful, not just truncated?
5. Word Limit: Does it meet the requirement?

SCORING GUIDE:
- 5/5: Perfect compression - essence captured beautifully, accurate, clear
- 4/5: Good compression - minor nuance lost but core intact
- 3/5: Acceptable - important element missing but still useful
- 2/5: Oversimplified - to the point of being misleading
- 1/5: Failed - essential meaning lost or factually incorrect

WORD LIMITS PROGRESSION:
100 → 50 → 25 → 15 (Tweet) → 10 (Sentence) → 1 (Single Word)"""

        user_prompt = f"""
TOPIC: {topic}
SUBJECT: {subject}
TARGET WORD LIMIT: {word_limit} words

{prev_context}

CURRENT COMPRESSION ATTEMPT:
"{compressed_explanation}"

Actual word count: {len(compressed_explanation.split())}

Evaluate this compression attempt and respond with ONLY a valid JSON object:
{{
    "score": <1-5>,
    "word_count": <actual word count>,
    "within_limit": <true/false>,
    "feedback": "<specific feedback on this compression>",
    "preserved_concepts": ["<list>", "<of>", "<preserved>", "<concepts>"],
    "lost_concepts": ["<list>", "<of>", "<lost>", "<concepts>"],
    "suggestion": "<how to improve or null if perfect>",
    "passed": <true if score >= 3 AND within word limit>,
    "next_word_limit": <next round's limit if passed, else null>
}}

Word limit progression: 100 → 50 → 25 → 15 → 10 → 1

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self._generate_text(system_prompt, user_prompt)
            result = self._parse_json_response(response)
            
            # Determine next word limit
            word_limits = [100, 50, 25, 15, 10, 1]
            current_idx = word_limits.index(word_limit) if word_limit in word_limits else 0
            next_limit = word_limits[current_idx + 1] if current_idx < len(word_limits) - 1 else None
            
            return CompressionEvaluation(
                score=int(result.get('score', 3)),
                word_count=len(compressed_explanation.split()),
                within_limit=len(compressed_explanation.split()) <= word_limit,
                feedback=result.get('feedback', 'Good attempt!'),
                preserved_concepts=result.get('preserved_concepts', []),
                lost_concepts=result.get('lost_concepts', []),
                suggestion=result.get('suggestion'),
                passed=result.get('passed', False),
                next_word_limit=next_limit if result.get('passed', False) else word_limit
            )
            
        except Exception as e:
            print(f"Error in evaluate_compression: {e}")
            return CompressionEvaluation(
                score=3,
                word_count=len(compressed_explanation.split()),
                within_limit=len(compressed_explanation.split()) <= word_limit,
                feedback="Let me evaluate your compression...",
                preserved_concepts=[],
                lost_concepts=[],
                suggestion="Try to focus on the most essential idea.",
                passed=False,
                next_word_limit=word_limit
            )
    
    # ============== LAYER 3: WHY SPIRAL ==============
    
    async def why_spiral_respond(
        self,
        topic: str,
        subject: str,
        current_depth: int,
        user_response: str,
        admits_unknown: bool,
        conversation_history: List[Dict[str, Any]]
    ) -> WhySpiralResponse:
        """Generate the next 'why' question or detect knowledge boundary"""
        
        context = self._build_conversation_context(conversation_history, layer=3)
        
        system_prompt = """You are a Socratic questioner conducting the "Why Spiral."
Your goal is to probe the student's understanding by asking progressive "why" questions.

SPIRAL DEPTH LEVELS:
- Level 1: Surface explanation (What happens?)
- Level 2: Mechanism (How does it happen?)
- Level 3: Causation (Why does it happen that way?)
- Level 4: Underlying principles (What fundamental law/principle governs this?)
- Level 5: Philosophical/Foundational (Why does that principle exist? What does it tell us about nature?)

RULES:
1. Each question must naturally follow from the student's previous answer
2. Go DEEPER into causation, not broader into scope
3. Questions should be genuinely probing, not trick questions
4. Be encouraging, not intimidating
5. If student reaches their knowledge boundary, acknowledge it warmly

BOUNDARY DETECTION - Triggers:
- Student says "I don't know" or "I'm not sure"
- Student gives circular reasoning (repeating earlier points)
- Student starts guessing without confidence
- Student's explanation becomes vague or hand-wavy
- Student explicitly admits they've reached their limit

When boundary is detected:
- Celebrate the discovery: "Excellent! You've found your learning edge!"
- Briefly explain what lies beyond (2-3 sentences, accessible)
- Offer to explore that area together"""

        user_prompt = f"""
TOPIC: {topic}
SUBJECT: {subject}
CURRENT DEPTH: Level {current_depth} of 5

CONVERSATION SO FAR:
{context if context else "Starting the Why Spiral."}

STUDENT'S RESPONSE:
"{user_response}"

STUDENT ADMITS THEY DON'T KNOW: {admits_unknown}

Generate the appropriate response. If this is the start (depth 1), ask the first "why" question.

Respond with ONLY a valid JSON object:
{{
    "next_question": "<the next 'why' question to ask, or null if boundary detected>",
    "current_depth": <1-5, the depth we're now at>,
    "reasoning": "<why this question follows logically from their answer>",
    "boundary_detected": <true/false>,
    "boundary_topic": "<the topic/concept where understanding ends, or null>",
    "exploration_offer": "<brief explanation of what's beyond + invitation to learn, or null>",
    "can_continue": <true if more questions possible, false if at depth 5 or boundary>
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self._generate_text(system_prompt, user_prompt)
            result = self._parse_json_response(response)
            
            return WhySpiralResponse(
                next_question=result.get('next_question'),
                current_depth=int(result.get('current_depth', current_depth)),
                reasoning=result.get('reasoning', ''),
                boundary_detected=result.get('boundary_detected', False),
                boundary_topic=result.get('boundary_topic'),
                exploration_offer=result.get('exploration_offer'),
                can_continue=result.get('can_continue', True)
            )
            
        except Exception as e:
            print(f"Error in why_spiral_respond: {e}")
            return WhySpiralResponse(
                next_question="Can you tell me more about why that is?",
                current_depth=current_depth,
                reasoning="Continuing the exploration.",
                boundary_detected=False,
                can_continue=True
            )
    
    # ============== LAYER 4: ANALOGY ARCHITECT ==============
    
    async def evaluate_analogy(
        self,
        topic: str,
        subject: str,
        analogy_text: str,
        phase: str,  # 'create', 'defend', 'refine'
        defense_response: Optional[str] = None,
        previous_feedback: Optional[str] = None
    ) -> AnalogyEvaluation:
        """Evaluate user's analogy and conduct stress test"""
        
        system_prompt = """You are an expert at evaluating educational analogies.
Good analogies should:
1. Map source domain concepts to target domain accurately
2. Be relatable to the learner's experience
3. Highlight the most important aspects of the concept
4. Not introduce misconceptions through false mappings
5. Be memorable and engaging

PHASES:
- CREATE: Initial evaluation of the analogy
- DEFEND: Test the analogy with challenging questions (devil's advocate)
- REFINE: Evaluate the refined version after feedback

STRESS TEST QUESTIONS should:
- Challenge false mappings (where the analogy breaks down)
- Ask about edge cases
- Probe for misconceptions the analogy might create
- Test if the analogy explains causation, not just correlation"""

        phase_instructions = {
            'create': """
This is the CREATE phase. Evaluate the analogy for the first time.
Identify strengths, weaknesses, and prepare a stress test question.""",
            'defend': f"""
This is the DEFEND phase. The student is defending their analogy.
Previous feedback: {previous_feedback}
Student's defense: {defense_response}
Evaluate whether their defense addresses the concerns.""",
            'refine': f"""
This is the REFINE phase. The student has refined their analogy.
Original feedback: {previous_feedback}
Evaluate the refined version."""
        }

        user_prompt = f"""
TOPIC: {topic}
SUBJECT: {subject}
PHASE: {phase}

ANALOGY:
"{analogy_text}"

{phase_instructions.get(phase, '')}

Respond with ONLY a valid JSON object:
{{
    "phase": "{phase}",
    "score": <1-5>,
    "strengths": ["<list>", "<of>", "<strengths>"],
    "weaknesses": ["<list>", "<of>", "<weaknesses>"],
    "stress_test_question": "<challenging question for defend phase, or null>",
    "passed_stress_test": <true/false if in defend phase, else null>,
    "refinement_suggestion": "<how to improve the analogy, or null if excellent>",
    "save_worthy": <true if score >= 4 and would help other learners>
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self._generate_text(system_prompt, user_prompt)
            result = self._parse_json_response(response)
            
            return AnalogyEvaluation(
                phase=phase,
                score=int(result.get('score', 3)),
                strengths=result.get('strengths', []),
                weaknesses=result.get('weaknesses', []),
                stress_test_question=result.get('stress_test_question'),
                passed_stress_test=result.get('passed_stress_test'),
                refinement_suggestion=result.get('refinement_suggestion'),
                save_worthy=result.get('save_worthy', False)
            )
            
        except Exception as e:
            print(f"Error in evaluate_analogy: {e}")
            return AnalogyEvaluation(
                phase=phase,
                score=3,
                strengths=["Creative attempt"],
                weaknesses=["Could be more specific"],
                stress_test_question="How does your analogy handle edge cases?",
                save_worthy=False
            )
    
    # ============== LAYER 5: LECTURE HALL ==============
    
    async def lecture_hall_respond(
        self,
        topic: str,
        subject: str,
        user_explanation: str,
        conversation_history: List[Dict[str, Any]]
    ) -> LectureHallResponse:
        """Get responses from all 5 Lecture Hall personas"""
        
        context = self._build_conversation_context(conversation_history, layer=5)
        
        system_prompt = """You control 5 different personas in a "Lecture Hall" setting.
Each persona has different needs and will evaluate the same explanation differently.

THE 5 PERSONAS:

1. DR. SKEPTIC (Professor)
   - Demands precision and accuracy
   - Challenges vague statements
   - Asks: "What's your evidence?" "That contradicts X, explain."
   - Satisfied by: rigorous, accurate explanations

2. THE PEDANT (Graduate Student)
   - Focuses on technical correctness
   - Catches oversimplifications
   - Says: "Well, technically..." "You're glossing over..."
   - Satisfied by: acknowledging nuance and complexity

3. CONFUSED CARL (Freshman Student)
   - Needs simple, clear explanations
   - Gets lost with jargon
   - Asks: "Wait, can you start over?" "What does that mean?"
   - Satisfied by: accessibility and clarity

4. INDUSTRY IAN (Practitioner)
   - Wants practical applications
   - Asks: "How does this apply in the real world?"
   - Says: "In my experience..." "But in practice..."
   - Satisfied by: real-world relevance and examples

5. LITTLE LILY (6-year-old)
   - Needs the simplest possible explanation
   - Asks endless "But why?" questions
   - Gets distracted, needs engagement
   - Satisfied by: fun, simple, relatable explanations

THE CHALLENGE:
The student must satisfy ALL personas simultaneously - balancing depth with accessibility,
technical accuracy with practical relevance, and rigor with simplicity."""

        user_prompt = f"""
TOPIC: {topic}
SUBJECT: {subject}

CONVERSATION SO FAR:
{context if context else "First explanation in the Lecture Hall."}

STUDENT'S EXPLANATION:
"{user_explanation}"

Generate responses from ALL 5 personas. Each should react based on their personality.

Respond with ONLY a valid JSON object:
{{
    "personas": [
        {{
            "persona": "dr_skeptic",
            "satisfaction": <0.0-1.0>,
            "response": "<Dr. Skeptic's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "the_pedant",
            "satisfaction": <0.0-1.0>,
            "response": "<The Pedant's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "confused_carl",
            "satisfaction": <0.0-1.0>,
            "response": "<Confused Carl's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "industry_ian",
            "satisfaction": <0.0-1.0>,
            "response": "<Industry Ian's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "little_lily",
            "satisfaction": <0.0-1.0>,
            "response": "<Little Lily's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }}
    ],
    "overall_satisfaction": <0.0-1.0, average of all>,
    "all_satisfied": <true only if ALL personas are satisfied>,
    "dominant_issue": "<main problem preventing full satisfaction, or null>",
    "suggestion": "<how to improve to satisfy everyone, or null if all satisfied>"
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self._generate_text(system_prompt, user_prompt)
            result = self._parse_json_response(response)
            
            personas = []
            for p in result.get('personas', []):
                personas.append(PersonaFeedback(
                    persona=LectureHallPersona(p.get('persona', 'confused_carl')),
                    satisfaction=float(p.get('satisfaction', 0.5)),
                    response=p.get('response', ''),
                    follow_up_question=p.get('follow_up_question'),
                    is_satisfied=p.get('is_satisfied', False)
                ))
            
            return LectureHallResponse(
                personas=personas,
                overall_satisfaction=float(result.get('overall_satisfaction', 0.5)),
                all_satisfied=result.get('all_satisfied', False),
                dominant_issue=result.get('dominant_issue'),
                suggestion=result.get('suggestion')
            )
            
        except Exception as e:
            print(f"Error in lecture_hall_respond: {e}")
            # Return default response
            return LectureHallResponse(
                personas=[
                    PersonaFeedback(
                        persona=LectureHallPersona.CONFUSED_CARL,
                        satisfaction=0.5,
                        response="I'm still trying to understand...",
                        is_satisfied=False
                    )
                ],
                overall_satisfaction=0.5,
                all_satisfied=False,
                dominant_issue="Need more clarity",
                suggestion="Try to simplify while maintaining accuracy."
            )
    
    # ============== HELPER METHODS ==============
    
    async def _generate_text(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text using Gemini text model"""
        
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
        
        response = self.text_model.generate_content(
            full_prompt,
            generation_config=self.json_generation_config
        )
        
        return response.text
    
    async def _generate_with_image(
        self, 
        system_prompt: str, 
        user_prompt: str,
        image_data: bytes,
        mime_type: str = "image/png"
    ) -> str:
        """Generate response using image model"""
        
        full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
        
        # Create image part
        image_part = {
            "mime_type": mime_type,
            "data": image_data
        }
        
        response = self.image_model.generate_content(
            [full_prompt, image_part],
            generation_config=self.json_generation_config
        )
        
        return response.text
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling potential formatting issues"""
        
        # Clean the response
        text = response.strip()
        
        # Remove markdown code blocks if present
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            
            # Return empty dict if parsing fails
            print(f"Failed to parse JSON: {text[:200]}...")
            return {}
    
    # ============== XP CALCULATION ==============
    
    def calculate_teaching_xp(
        self,
        layer_completed: int,
        clarity_score: float,
        compression_rounds_passed: int,
        why_depth_reached: int,
        analogy_saved: bool,
        all_personas_satisfied: bool,
        gaps_discovered: int
    ) -> Tuple[int, List[str]]:
        """Calculate Teaching XP earned and achievements unlocked"""
        
        xp = 0
        achievements = []
        
        # Layer completion XP
        layer_xp = {1: 50, 2: 75, 3: 100, 4: 150, 5: 200}
        xp += layer_xp.get(layer_completed, 0)
        
        # Clarity bonus
        if clarity_score >= 90:
            xp += 100
            achievements.append("Crystal Clear Explanation")
        elif clarity_score >= 75:
            xp += 50
        
        # Compression bonus
        xp += compression_rounds_passed * 30
        if compression_rounds_passed >= 6:
            achievements.append("Master Compressor")
        
        # Why Spiral depth bonus
        xp += why_depth_reached * 25
        if why_depth_reached >= 5:
            achievements.append("Deep Diver")
        
        # Analogy bonus
        if analogy_saved:
            xp += 100
            achievements.append("Analogy Architect")
        
        # Lecture Hall bonus
        if all_personas_satisfied:
            xp += 200
            achievements.append("Master Communicator")
        
        # Gap discovery bonus
        xp += gaps_discovered * 15
        if gaps_discovered >= 5:
            achievements.append("Gap Hunter")
        
        return xp, achievements


# Singleton instance
feynman_ai = FeynmanAIService()
```

---

## 8. API ENDPOINTS

### 8.1 API Router (backend/app/api/feynman.py)

```python
"""
FastAPI Router for Feynman Engine endpoints
"""

import json
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

from ..models.feynman_models import (
    StartSessionRequest, TeachMessageRequest, TeachWithImageRequest,
    CompressionSubmitRequest, WhySpiralResponseRequest, AnalogySubmitRequest,
    LectureHallMessageRequest, RateAnalogyRequest,
    ChintuResponse, CompressionEvaluation, WhySpiralResponse,
    AnalogyEvaluation, LectureHallResponse, SessionResponse,
    SessionSummary, GapResponse, AnalogyListItem,
    FeynmanLayer, SessionStatus
)
from ..services.feynman_service import feynman_ai
from ..database.feynman_db import feynman_db


router = APIRouter(prefix="/api/feynman", tags=["Feynman Engine"])


# ============== SESSION ENDPOINTS ==============

@router.post("/session/start", response_model=SessionResponse)
async def start_session(request: StartSessionRequest):
    """Start a new Feynman Engine session"""
    
    try:
        session = feynman_db.create_session(
            user_id=request.user_id,
            topic=request.topic,
            subject=request.subject,
            difficulty_level=request.difficulty_level,
            starting_layer=request.starting_layer.value
        )
        
        return SessionResponse(
            session_id=session['id'],
            user_id=session['user_id'],
            topic=session['topic'],
            subject=session['subject'],
            difficulty_level=session['difficulty_level'],
            current_layer=session['current_layer'],
            status=SessionStatus.ACTIVE,
            clarity_score=0.0,
            teaching_xp_earned=0,
            started_at=datetime.fromisoformat(session['started_at']),
            completed_at=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get session details"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        session_id=session['id'],
        user_id=session['user_id'],
        topic=session['topic'],
        subject=session['subject'],
        difficulty_level=session['difficulty_level'],
        current_layer=session['current_layer'],
        status=SessionStatus(session['status']),
        clarity_score=float(session.get('clarity_score', 0)),
        teaching_xp_earned=int(session.get('teaching_xp_earned', 0)),
        started_at=datetime.fromisoformat(session['started_at']),
        completed_at=datetime.fromisoformat(session['completed_at']) if session.get('completed_at') else None
    )


@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, layer: Optional[int] = None):
    """Get conversation history for a session"""
    
    history = feynman_db.get_conversation_history(session_id, layer)
    return {"session_id": session_id, "history": history}


@router.post("/session/{session_id}/complete", response_model=SessionSummary)
async def complete_session(session_id: str):
    """Complete a session and get summary"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Calculate final XP
    gaps = feynman_db.get_user_gaps(session['user_id'])
    session_gaps = [g for g in gaps if g['session_id'] == session_id]
    
    compression_rounds = 0  # Calculate from history
    history = feynman_db.get_conversation_history(session_id, layer=2)
    compression_rounds = len([h for h in history if h['role'] == 'user'])
    
    xp, achievements = feynman_ai.calculate_teaching_xp(
        layer_completed=session.get('current_layer', 1),
        clarity_score=float(session.get('clarity_score', 0)),
        compression_rounds_passed=compression_rounds,
        why_depth_reached=int(session.get('why_depth_reached', 0)),
        analogy_saved=float(session.get('analogy_score', 0)) >= 4,
        all_personas_satisfied=False,  # Check from history
        gaps_discovered=len(session_gaps)
    )
    
    # Update session
    feynman_db.update_session(session_id, {
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat(),
        'teaching_xp_earned': xp
    })
    
    # Calculate total time
    started = datetime.fromisoformat(session['started_at'])
    total_minutes = (datetime.utcnow() - started).total_seconds() / 60
    
    # Build gap responses
    gap_responses = [
        GapResponse(
            gap_id=g['id'],
            topic=g['gap_topic'],
            description=g['gap_description'],
            layer_discovered=g['layer_discovered'],
            why_depth=g.get('why_depth'),
            resolved=g['resolved']
        )
        for g in session_gaps
    ]
    
    return SessionSummary(
        session_id=session_id,
        topic=session['topic'],
        total_time_minutes=round(total_minutes, 1),
        layers_completed=list(range(1, session.get('current_layer', 1) + 1)),
        final_clarity_score=float(session.get('clarity_score', 0)),
        compression_score=float(session.get('compression_score')) if session.get('compression_score') else None,
        analogy_score=float(session.get('analogy_score')) if session.get('analogy_score') else None,
        why_depth_reached=int(session.get('why_depth_reached', 0)),
        gaps_discovered=gap_responses,
        teaching_xp_earned=xp,
        achievements_unlocked=achievements
    )


@router.get("/sessions/user/{user_id}")
async def get_user_sessions(
    user_id: str, 
    status: Optional[str] = None,
    limit: int = 20
):
    """Get all sessions for a user"""
    
    sessions = feynman_db.get_user_sessions(user_id, status, limit)
    return {"user_id": user_id, "sessions": sessions}


# ============== LAYER 1: CHINTU (CURIOUS CHILD) ==============

@router.post("/layer1/teach", response_model=ChintuResponse)
async def teach_chintu(request: TeachMessageRequest):
    """Send a teaching message to Chintu"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="user",
        message=request.message
    )
    
    # Get conversation history
    history = feynman_db.get_conversation_history(request.session_id, layer=1)
    
    # Get AI response
    response = await feynman_ai.chintu_respond(
        session_id=request.session_id,
        topic=session['topic'],
        subject=session['subject'],
        user_message=request.message,
        conversation_history=history,
        difficulty_level=session['difficulty_level']
    )
    
    # Save AI response
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="assistant",
        message=response.response,
        confusion_level=response.confusion_level,
        curiosity_level=response.curiosity_level,
        question_type=response.question_type.value,
        gap_detected=response.gap_detected
    )
    
    # If gap detected, save it
    if response.gap_detected:
        feynman_db.add_gap(
            session_id=request.session_id,
            user_id=session['user_id'],
            gap_topic=response.gap_detected,
            gap_description=f"Gap detected while explaining {session['topic']}",
            layer_discovered=1
        )
    
    # Update clarity score (inverse of average confusion)
    clarity = (1 - response.confusion_level) * 100
    feynman_db.update_session(request.session_id, {'clarity_score': clarity})
    
    # If layer complete, update current_layer
    if response.layer_complete:
        feynman_db.update_session(request.session_id, {'current_layer': 2})
    
    return response


@router.post("/layer1/teach-with-image", response_model=ChintuResponse)
async def teach_chintu_with_image(request: TeachWithImageRequest):
    """Send a teaching message with an image to Chintu"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="user",
        message=request.message,
        image_url="[image attached]"
    )
    
    # Get conversation history
    history = feynman_db.get_conversation_history(request.session_id, layer=1)
    
    # Get AI response with image
    response = await feynman_ai.chintu_respond(
        session_id=request.session_id,
        topic=session['topic'],
        subject=session['subject'],
        user_message=request.message,
        conversation_history=history,
        difficulty_level=session['difficulty_level'],
        image_base64=request.image_base64,
        image_mime_type=request.image_mime_type
    )
    
    # Save AI response
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="assistant",
        message=response.response,
        confusion_level=response.confusion_level,
        curiosity_level=response.curiosity_level,
        question_type=response.question_type.value,
        gap_detected=response.gap_detected
    )
    
    return response


# ============== LAYER 2: COMPRESSION CHALLENGE ==============

@router.post("/layer2/compress", response_model=CompressionEvaluation)
async def submit_compression(request: CompressionSubmitRequest):
    """Submit a compression challenge attempt"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user attempt
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=2,
        role="user",
        message=f"[{request.word_limit} words]: {request.explanation}"
    )
    
    # Get previous compressions
    history = feynman_db.get_conversation_history(request.session_id, layer=2)
    previous = [
        {
            'word_limit': int(h['message'].split(']')[0].replace('[', '').split()[0]),
            'explanation': h['message'].split(']: ')[1] if ']: ' in h['message'] else h['message'],
            'score': 3  # Default, could parse from assistant responses
        }
        for h in history if h['role'] == 'user' and h['message'] != f"[{request.word_limit} words]: {request.explanation}"
    ]
    
    # Get evaluation
    evaluation = await feynman_ai.evaluate_compression(
        topic=session['topic'],
        subject=session['subject'],
        original_explanation="",  # Could be stored from Layer 1
        compressed_explanation=request.explanation,
        word_limit=request.word_limit,
        previous_compressions=previous
    )
    
    # Save evaluation
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=2,
        role="assistant",
        message=f"Score: {evaluation.score}/5 - {evaluation.feedback}"
    )
    
    # Update compression score
    feynman_db.update_session(request.session_id, {
        'compression_score': evaluation.score * 20  # Convert to 0-100
    })
    
    # If completed all rounds, move to layer 3
    if evaluation.passed and evaluation.next_word_limit == 1:
        feynman_db.update_session(request.session_id, {'current_layer': 3})
    
    return evaluation


# ============== LAYER 3: WHY SPIRAL ==============

@router.post("/layer3/start")
async def start_why_spiral(session_id: str):
    """Start the Why Spiral with the first question"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate first question
    response = await feynman_ai.why_spiral_respond(
        topic=session['topic'],
        subject=session['subject'],
        current_depth=1,
        user_response="",
        admits_unknown=False,
        conversation_history=[]
    )
    
    # Save the first question
    feynman_db.add_conversation_turn(
        session_id=session_id,
        layer=3,
        role="assistant",
        message=response.next_question or f"Let's explore why {session['topic']} works the way it does. Can you start by explaining the basic concept?"
    )
    
    return response


@router.post("/layer3/respond", response_model=WhySpiralResponse)
async def respond_why_spiral(request: WhySpiralResponseRequest):
    """Respond to a Why Spiral question"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user response
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=3,
        role="user",
        message=request.response if not request.admits_unknown else f"[I don't know] {request.response}"
    )
    
    # Get history
    history = feynman_db.get_conversation_history(request.session_id, layer=3)
    current_depth = len([h for h in history if h['role'] == 'assistant']) + 1
    
    # Get next question or detect boundary
    response = await feynman_ai.why_spiral_respond(
        topic=session['topic'],
        subject=session['subject'],
        current_depth=current_depth,
        user_response=request.response,
        admits_unknown=request.admits_unknown,
        conversation_history=history
    )
    
    # Save AI response
    if response.next_question:
        feynman_db.add_conversation_turn(
            session_id=request.session_id,
            layer=3,
            role="assistant",
            message=response.next_question
        )
    elif response.boundary_detected:
        feynman_db.add_conversation_turn(
            session_id=request.session_id,
            layer=3,
            role="assistant",
            message=f"🎯 Knowledge boundary found: {response.boundary_topic}\n\n{response.exploration_offer}"
        )
        
        # Save the gap
        feynman_db.add_gap(
            session_id=request.session_id,
            user_id=session['user_id'],
            gap_topic=response.boundary_topic,
            gap_description=response.exploration_offer or "",
            layer_discovered=3,
            why_depth=response.current_depth
        )
    
    # Update why depth
    feynman_db.update_session(request.session_id, {
        'why_depth_reached': response.current_depth
    })
    
    # If boundary detected or reached level 5, move to layer 4
    if response.boundary_detected or response.current_depth >= 5:
        feynman_db.update_session(request.session_id, {'current_layer': 4})
    
    return response


# ============== LAYER 4: ANALOGY ARCHITECT ==============

@router.post("/layer4/submit", response_model=AnalogyEvaluation)
async def submit_analogy(request: AnalogySubmitRequest):
    """Submit or refine an analogy"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user submission
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=4,
        role="user",
        message=f"[{request.phase}]: {request.analogy_text}"
    )
    
    # Get previous feedback if any
    history = feynman_db.get_conversation_history(request.session_id, layer=4)
    previous_feedback = None
    for h in reversed(history):
        if h['role'] == 'assistant':
            previous_feedback = h['message']
            break
    
    # Evaluate
    evaluation = await feynman_ai.evaluate_analogy(
        topic=session['topic'],
        subject=session['subject'],
        analogy_text=request.analogy_text,
        phase=request.phase,
        defense_response=request.defense_response,
        previous_feedback=previous_feedback
    )
    
    # Save evaluation
    feedback_msg = f"Score: {evaluation.score}/5\n"
    feedback_msg += f"Strengths: {', '.join(evaluation.strengths)}\n"
    feedback_msg += f"Weaknesses: {', '.join(evaluation.weaknesses)}\n"
    if evaluation.stress_test_question:
        feedback_msg += f"\n🔥 Stress Test: {evaluation.stress_test_question}"
    
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=4,
        role="assistant",
        message=feedback_msg
    )
    
    # Update analogy score
    feynman_db.update_session(request.session_id, {
        'analogy_score': evaluation.score * 20
    })
    
    # If save-worthy, save to analogies database
    if evaluation.save_worthy and request.phase == 'refine':
        feynman_db.save_analogy(
            user_id=session['user_id'],
            topic=session['topic'],
            subject=session['subject'],
            analogy_text=request.analogy_text,
            stress_test_passed=evaluation.passed_stress_test or False
        )
    
    # If passed, move to layer 5
    if evaluation.score >= 4 and request.phase == 'refine':
        feynman_db.update_session(request.session_id, {'current_layer': 5})
    
    return evaluation


# ============== LAYER 5: LECTURE HALL ==============

@router.post("/layer5/teach", response_model=LectureHallResponse)
async def teach_lecture_hall(request: LectureHallMessageRequest):
    """Send explanation to all Lecture Hall personas"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=5,
        role="user",
        message=request.message
    )
    
    # Get history
    history = feynman_db.get_conversation_history(request.session_id, layer=5)
    
    # Get responses from all personas
    response = await feynman_ai.lecture_hall_respond(
        topic=session['topic'],
        subject=session['subject'],
        user_explanation=request.message,
        conversation_history=history
    )
    
    # Save all persona responses
    for persona in response.personas:
        feynman_db.add_conversation_turn(
            session_id=request.session_id,
            layer=5,
            role="assistant",
            message=f"[{persona.persona.value}]: {persona.response}"
        )
    
    return response


# ============== GAP ENDPOINTS ==============

@router.get("/gaps/user/{user_id}")
async def get_user_gaps(
    user_id: str,
    resolved: Optional[bool] = None
):
    """Get knowledge gaps for a user"""
    
    gaps = feynman_db.get_user_gaps(user_id, resolved)
    return {"user_id": user_id, "gaps": gaps}


@router.post("/gaps/{gap_id}/resolve")
async def resolve_gap(gap_id: str, linked_session_id: Optional[str] = None):
    """Mark a gap as resolved"""
    
    success = feynman_db.resolve_gap(gap_id, linked_session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gap not found")
    
    return {"status": "resolved", "gap_id": gap_id}


# ============== ANALOGY ENDPOINTS ==============

@router.get("/analogies", response_model=List[AnalogyListItem])
async def get_analogies(
    topic: Optional[str] = None,
    subject: Optional[str] = None,
    featured_only: bool = False,
    limit: int = 20
):
    """Get community analogies"""
    
    analogies = feynman_db.get_analogies(topic, subject, featured_only, limit)
    return [
        AnalogyListItem(
            id=a['id'],
            topic=a['topic'],
            subject=a['subject'],
            analogy_text=a['analogy_text'],
            creator_username=None,  # Would need to join with users
            community_rating=float(a.get('community_rating', 0)),
            upvotes=int(a.get('upvotes', 0)),
            is_featured=bool(a.get('is_featured', False))
        )
        for a in analogies
    ]


@router.post("/analogies/{analogy_id}/vote")
async def vote_analogy(analogy_id: str, vote_type: str):
    """Upvote or downvote an analogy"""
    
    if vote_type not in ['upvote', 'downvote']:
        raise HTTPException(status_code=400, detail="vote_type must be 'upvote' or 'downvote'")
    
    success = feynman_db.vote_analogy(analogy_id, vote_type)
    if not success:
        raise HTTPException(status_code=404, detail="Analogy not found")
    
    return {"status": "voted", "analogy_id": analogy_id, "vote_type": vote_type}


# ============== SUBJECTS & TOPICS ==============

@router.get("/subjects")
async def get_subjects():
    """Get list of available subjects"""
    
    return {
        "subjects": [
            "Physics",
            "Chemistry",
            "Biology",
            "Mathematics",
            "History",
            "Geography",
            "Computer Science",
            "Economics",
            "English",
            "Hindi",
            "General Knowledge"
        ]
    }


@router.get("/topics/suggestions")
async def get_topic_suggestions(subject: Optional[str] = None, query: Optional[str] = None):
    """Get topic suggestions based on subject or search query"""
    
    # This could be expanded with a proper topics database
    topic_suggestions = {
        "Physics": ["Newton's Laws", "Gravity", "Light", "Sound", "Electricity", "Magnetism"],
        "Chemistry": ["Atoms", "Chemical Bonds", "Acids and Bases", "Periodic Table"],
        "Biology": ["Photosynthesis", "Cells", "DNA", "Evolution", "Human Body"],
        "Mathematics": ["Fractions", "Algebra", "Geometry", "Trigonometry", "Calculus"],
        "History": ["World War 2", "French Revolution", "Ancient India", "Independence Movement"],
        "Geography": ["Climate", "Rivers", "Mountains", "Solar System", "Continents"],
        "Computer Science": ["Algorithms", "Data Structures", "Networks", "Programming"]
    }
    
    if subject and subject in topic_suggestions:
        topics = topic_suggestions[subject]
    else:
        topics = [topic for topics in topic_suggestions.values() for topic in topics]
    
    if query:
        topics = [t for t in topics if query.lower() in t.lower()]
    
    return {"topics": topics[:20]}
```

### 8.2 Register Router in Main App

Add to `backend/app/main.py`:

```python
from app.api import feynman

# Add this line where other routers are included
app.include_router(feynman.router)
```

---

## 9. FRONTEND IMPLEMENTATION

### 9.1 TypeScript Types (frontend/src/types/feynman.ts)

```typescript
/**
 * TypeScript types for Feynman Engine
 */

export enum FeynmanLayer {
  CURIOUS_CHILD = 1,
  COMPRESSION = 2,
  WHY_SPIRAL = 3,
  ANALOGY_ARCHITECT = 4,
  LECTURE_HALL = 5,
}

export enum SessionStatus {
  ACTIVE = 'active',
  COMPLETED = 'completed',
  ABANDONED = 'abandoned',
}

export enum QuestionType {
  CLARIFYING = 'clarifying',
  CURIOUS = 'curious',
  CHALLENGING = 'challenging',
  CONFUSED = 'confused',
}

export enum LectureHallPersona {
  DR_SKEPTIC = 'dr_skeptic',
  THE_PEDANT = 'the_pedant',
  CONFUSED_CARL = 'confused_carl',
  INDUSTRY_IAN = 'industry_ian',
  LITTLE_LILY = 'little_lily',
}

// Request Types
export interface StartSessionRequest {
  user_id: string;
  topic: string;
  subject: string;
  difficulty_level?: number;
  starting_layer?: FeynmanLayer;
}

export interface TeachMessageRequest {
  session_id: string;
  message: string;
  layer: FeynmanLayer;
}

export interface TeachWithImageRequest extends TeachMessageRequest {
  image_base64: string;
  image_mime_type?: string;
}

export interface CompressionSubmitRequest {
  session_id: string;
  word_limit: number;
  explanation: string;
}

export interface WhySpiralResponseRequest {
  session_id: string;
  response: string;
  admits_unknown?: boolean;
}

export interface AnalogySubmitRequest {
  session_id: string;
  analogy_text: string;
  phase: 'create' | 'defend' | 'refine';
  defense_response?: string;
}

export interface LectureHallMessageRequest {
  session_id: string;
  message: string;
}

// Response Types
export interface ChintuResponse {
  response: string;
  confusion_level: number;
  curiosity_level: number;
  question_type: QuestionType;
  follow_up_question?: string;
  gap_detected?: string;
  encouragement?: string;
  emoji_reaction: string;
  layer_complete: boolean;
}

export interface CompressionEvaluation {
  score: number;
  word_count: number;
  within_limit: boolean;
  feedback: string;
  preserved_concepts: string[];
  lost_concepts: string[];
  suggestion?: string;
  passed: boolean;
  next_word_limit?: number;
}

export interface WhySpiralResponse {
  next_question?: string;
  current_depth: number;
  reasoning: string;
  boundary_detected: boolean;
  boundary_topic?: string;
  exploration_offer?: string;
  can_continue: boolean;
}

export interface AnalogyEvaluation {
  phase: string;
  score: number;
  strengths: string[];
  weaknesses: string[];
  stress_test_question?: string;
  passed_stress_test?: boolean;
  refinement_suggestion?: string;
  save_worthy: boolean;
}

export interface PersonaFeedback {
  persona: LectureHallPersona;
  satisfaction: number;
  response: string;
  follow_up_question?: string;
  is_satisfied: boolean;
}

export interface LectureHallResponse {
  personas: PersonaFeedback[];
  overall_satisfaction: number;
  all_satisfied: boolean;
  dominant_issue?: string;
  suggestion?: string;
}

export interface SessionResponse {
  session_id: string;
  user_id: string;
  topic: string;
  subject: string;
  difficulty_level: number;
  current_layer: number;
  status: SessionStatus;
  clarity_score: number;
  teaching_xp_earned: number;
  started_at: string;
  completed_at?: string;
}

export interface GapResponse {
  gap_id: string;
  topic: string;
  description: string;
  layer_discovered: number;
  why_depth?: number;
  resolved: boolean;
}

export interface SessionSummary {
  session_id: string;
  topic: string;
  total_time_minutes: number;
  layers_completed: number[];
  final_clarity_score: number;
  compression_score?: number;
  analogy_score?: number;
  why_depth_reached: number;
  gaps_discovered: GapResponse[];
  teaching_xp_earned: number;
  achievements_unlocked: string[];
}

export interface ConversationTurn {
  role: 'user' | 'assistant';
  message: string;
  layer: number;
  turn_number: number;
  confusion_level?: number;
  curiosity_level?: number;
  image_url?: string;
}

export interface AnalogyListItem {
  id: string;
  topic: string;
  subject: string;
  analogy_text: string;
  creator_username?: string;
  community_rating: number;
  upvotes: number;
  is_featured: boolean;
}

// Store State
export interface FeynmanState {
  currentSession: SessionResponse | null;
  conversationHistory: ConversationTurn[];
  isLoading: boolean;
  error: string | null;
  
  // Layer-specific state
  chintuConfusion: number;
  chintuCuriosity: number;
  compressionRound: number;
  whySpiralDepth: number;
  analogyPhase: 'create' | 'defend' | 'refine' | null;
  lectureHallPersonas: PersonaFeedback[];
  
  // Gaps
  discoveredGaps: GapResponse[];
}
```

### 9.2 API Service (frontend/src/services/feynmanService.ts)

```typescript
/**
 * API Service for Feynman Engine
 */

import axios from 'axios';
import type {
  StartSessionRequest,
  TeachMessageRequest,
  TeachWithImageRequest,
  CompressionSubmitRequest,
  WhySpiralResponseRequest,
  AnalogySubmitRequest,
  LectureHallMessageRequest,
  ChintuResponse,
  CompressionEvaluation,
  WhySpiralResponse,
  AnalogyEvaluation,
  LectureHallResponse,
  SessionResponse,
  SessionSummary,
  GapResponse,
  AnalogyListItem,
} from '../types/feynman';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE}/api/feynman`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============== SESSION ENDPOINTS ==============

export const startSession = async (
  request: StartSessionRequest
): Promise<SessionResponse> => {
  const response = await api.post('/session/start', request);
  return response.data;
};

export const getSession = async (sessionId: string): Promise<SessionResponse> => {
  const response = await api.get(`/session/${sessionId}`);
  return response.data;
};

export const getSessionHistory = async (
  sessionId: string,
  layer?: number
): Promise<{ session_id: string; history: any[] }> => {
  const params = layer ? { layer } : {};
  const response = await api.get(`/session/${sessionId}/history`, { params });
  return response.data;
};

export const completeSession = async (
  sessionId: string
): Promise<SessionSummary> => {
  const response = await api.post(`/session/${sessionId}/complete`);
  return response.data;
};

export const getUserSessions = async (
  userId: string,
  status?: string,
  limit: number = 20
): Promise<{ user_id: string; sessions: SessionResponse[] }> => {
  const params = { status, limit };
  const response = await api.get(`/sessions/user/${userId}`, { params });
  return response.data;
};

// ============== LAYER 1: CHINTU ==============

export const teachChintu = async (
  request: TeachMessageRequest
): Promise<ChintuResponse> => {
  const response = await api.post('/layer1/teach', request);
  return response.data;
};

export const teachChintuWithImage = async (
  request: TeachWithImageRequest
): Promise<ChintuResponse> => {
  const response = await api.post('/layer1/teach-with-image', request);
  return response.data;
};

// ============== LAYER 2: COMPRESSION ==============

export const submitCompression = async (
  request: CompressionSubmitRequest
): Promise<CompressionEvaluation> => {
  const response = await api.post('/layer2/compress', request);
  return response.data;
};

// ============== LAYER 3: WHY SPIRAL ==============

export const startWhySpiral = async (
  sessionId: string
): Promise<WhySpiralResponse> => {
  const response = await api.post(`/layer3/start?session_id=${sessionId}`);
  return response.data;
};

export const respondWhySpiral = async (
  request: WhySpiralResponseRequest
): Promise<WhySpiralResponse> => {
  const response = await api.post('/layer3/respond', request);
  return response.data;
};

// ============== LAYER 4: ANALOGY ==============

export const submitAnalogy = async (
  request: AnalogySubmitRequest
): Promise<AnalogyEvaluation> => {
  const response = await api.post('/layer4/submit', request);
  return response.data;
};

// ============== LAYER 5: LECTURE HALL ==============

export const teachLectureHall = async (
  request: LectureHallMessageRequest
): Promise<LectureHallResponse> => {
  const response = await api.post('/layer5/teach', request);
  return response.data;
};

// ============== GAPS ==============

export const getUserGaps = async (
  userId: string,
  resolved?: boolean
): Promise<{ user_id: string; gaps: GapResponse[] }> => {
  const params = resolved !== undefined ? { resolved } : {};
  const response = await api.get(`/gaps/user/${userId}`, { params });
  return response.data;
};

export const resolveGap = async (
  gapId: string,
  linkedSessionId?: string
): Promise<{ status: string; gap_id: string }> => {
  const params = linkedSessionId ? { linked_session_id: linkedSessionId } : {};
  const response = await api.post(`/gaps/${gapId}/resolve`, null, { params });
  return response.data;
};

// ============== ANALOGIES ==============

export const getAnalogies = async (
  topic?: string,
  subject?: string,
  featuredOnly: boolean = false,
  limit: number = 20
): Promise<AnalogyListItem[]> => {
  const params = { topic, subject, featured_only: featuredOnly, limit };
  const response = await api.get('/analogies', { params });
  return response.data;
};

export const voteAnalogy = async (
  analogyId: string,
  voteType: 'upvote' | 'downvote'
): Promise<{ status: string; analogy_id: string; vote_type: string }> => {
  const response = await api.post(
    `/analogies/${analogyId}/vote?vote_type=${voteType}`
  );
  return response.data;
};

// ============== UTILITIES ==============

export const getSubjects = async (): Promise<{ subjects: string[] }> => {
  const response = await api.get('/subjects');
  return response.data;
};

export const getTopicSuggestions = async (
  subject?: string,
  query?: string
): Promise<{ topics: string[] }> => {
  const params = { subject, query };
  const response = await api.get('/topics/suggestions', { params });
  return response.data;
};

// Helper to convert file to base64
export const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const result = reader.result as string;
      // Remove the data URL prefix (e.g., "data:image/png;base64,")
      const base64 = result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = (error) => reject(error);
  });
};

export default {
  startSession,
  getSession,
  getSessionHistory,
  completeSession,
  getUserSessions,
  teachChintu,
  teachChintuWithImage,
  submitCompression,
  startWhySpiral,
  respondWhySpiral,
  submitAnalogy,
  teachLectureHall,
  getUserGaps,
  resolveGap,
  getAnalogies,
  voteAnalogy,
  getSubjects,
  getTopicSuggestions,
  fileToBase64,
};
```

### 9.3 Zustand Store (frontend/src/store/feynmanStore.ts)

```typescript
/**
 * Zustand store for Feynman Engine state management
 */

import { create } from 'zustand';
import type {
  FeynmanState,
  SessionResponse,
  ConversationTurn,
  GapResponse,
  PersonaFeedback,
  ChintuResponse,
  CompressionEvaluation,
  WhySpiralResponse,
  AnalogyEvaluation,
  LectureHallResponse,
} from '../types/feynman';
import * as feynmanService from '../services/feynmanService';

interface FeynmanStore extends FeynmanState {
  // Actions
  startNewSession: (
    userId: string,
    topic: string,
    subject: string,
    difficulty?: number
  ) => Promise<void>;
  loadSession: (sessionId: string) => Promise<void>;
  
  // Layer 1
  sendToChintu: (message: string, imageBase64?: string) => Promise<ChintuResponse>;
  
  // Layer 2
  submitCompression: (wordLimit: number, explanation: string) => Promise<CompressionEvaluation>;
  
  // Layer 3
  startWhySpiral: () => Promise<WhySpiralResponse>;
  respondToWhy: (response: string, admitsUnknown?: boolean) => Promise<WhySpiralResponse>;
  
  // Layer 4
  submitAnalogy: (
    text: string,
    phase: 'create' | 'defend' | 'refine',
    defenseResponse?: string
  ) => Promise<AnalogyEvaluation>;
  
  // Layer 5
  teachLectureHall: (message: string) => Promise<LectureHallResponse>;
  
  // Session management
  completeSession: () => Promise<void>;
  resetState: () => void;
  setError: (error: string | null) => void;
  
  // Helpers
  addConversationTurn: (turn: ConversationTurn) => void;
  updateChintuMetrics: (confusion: number, curiosity: number) => void;
}

const initialState: FeynmanState = {
  currentSession: null,
  conversationHistory: [],
  isLoading: false,
  error: null,
  chintuConfusion: 0.5,
  chintuCuriosity: 0.5,
  compressionRound: 1,
  whySpiralDepth: 0,
  analogyPhase: null,
  lectureHallPersonas: [],
  discoveredGaps: [],
};

export const useFeynmanStore = create<FeynmanStore>((set, get) => ({
  ...initialState,

  // Start a new session
  startNewSession: async (userId, topic, subject, difficulty = 5) => {
    set({ isLoading: true, error: null });
    try {
      const session = await feynmanService.startSession({
        user_id: userId,
        topic,
        subject,
        difficulty_level: difficulty,
      });
      set({
        currentSession: session,
        conversationHistory: [],
        isLoading: false,
        chintuConfusion: 0.5,
        chintuCuriosity: 0.5,
        compressionRound: 1,
        whySpiralDepth: 0,
        analogyPhase: null,
        lectureHallPersonas: [],
        discoveredGaps: [],
      });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Load existing session
  loadSession: async (sessionId) => {
    set({ isLoading: true, error: null });
    try {
      const session = await feynmanService.getSession(sessionId);
      const historyData = await feynmanService.getSessionHistory(sessionId);
      
      const history: ConversationTurn[] = historyData.history.map((h: any) => ({
        role: h.role,
        message: h.message,
        layer: h.layer,
        turn_number: h.turn_number,
        confusion_level: h.confusion_level,
        curiosity_level: h.curiosity_level,
        image_url: h.image_url,
      }));
      
      set({
        currentSession: session,
        conversationHistory: history,
        isLoading: false,
      });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 1: Send message to Chintu
  sendToChintu: async (message, imageBase64) => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });
    
    try {
      // Add user message to history
      get().addConversationTurn({
        role: 'user',
        message,
        layer: 1,
        turn_number: get().conversationHistory.filter(t => t.layer === 1).length + 1,
      });

      let response: ChintuResponse;
      
      if (imageBase64) {
        response = await feynmanService.teachChintuWithImage({
          session_id: currentSession.session_id,
          message,
          layer: 1,
          image_base64: imageBase64,
          image_mime_type: 'image/png',
        });
      } else {
        response = await feynmanService.teachChintu({
          session_id: currentSession.session_id,
          message,
          layer: 1,
        });
      }

      // Add Chintu's response to history
      get().addConversationTurn({
        role: 'assistant',
        message: response.response,
        layer: 1,
        turn_number: get().conversationHistory.filter(t => t.layer === 1).length + 1,
        confusion_level: response.confusion_level,
        curiosity_level: response.curiosity_level,
      });

      // Update metrics
      get().updateChintuMetrics(response.confusion_level, response.curiosity_level);

      // If gap detected, add to gaps
      if (response.gap_detected) {
        set(state => ({
          discoveredGaps: [
            ...state.discoveredGaps,
            {
              gap_id: `temp-${Date.now()}`,
              topic: response.gap_detected!,
              description: 'Gap detected during explanation',
              layer_discovered: 1,
              resolved: false,
            },
          ],
        }));
      }

      // If layer complete, update session
      if (response.layer_complete) {
        set(state => ({
          currentSession: state.currentSession
            ? { ...state.currentSession, current_layer: 2 }
            : null,
        }));
      }

      set({ isLoading: false });
      return response;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 2: Submit compression
  submitCompression: async (wordLimit, explanation) => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });

    try {
      get().addConversationTurn({
        role: 'user',
        message: `[${wordLimit} words]: ${explanation}`,
        layer: 2,
        turn_number: get().conversationHistory.filter(t => t.layer === 2).length + 1,
      });

      const response = await feynmanService.submitCompression({
        session_id: currentSession.session_id,
        word_limit: wordLimit,
        explanation,
      });

      get().addConversationTurn({
        role: 'assistant',
        message: `Score: ${response.score}/5 - ${response.feedback}`,
        layer: 2,
        turn_number: get().conversationHistory.filter(t => t.layer === 2).length + 1,
      });

      if (response.passed && response.next_word_limit) {
        set(state => ({ compressionRound: state.compressionRound + 1 }));
      }

      // Check if all rounds complete
      if (response.passed && response.next_word_limit === 1) {
        set(state => ({
          currentSession: state.currentSession
            ? { ...state.currentSession, current_layer: 3 }
            : null,
        }));
      }

      set({ isLoading: false });
      return response;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 3: Start Why Spiral
  startWhySpiral: async () => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });

    try {
      const response = await feynmanService.startWhySpiral(currentSession.session_id);

      if (response.next_question) {
        get().addConversationTurn({
          role: 'assistant',
          message: response.next_question,
          layer: 3,
          turn_number: 1,
        });
      }

      set({ whySpiralDepth: 1, isLoading: false });
      return response;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 3: Respond to Why
  respondToWhy: async (response, admitsUnknown = false) => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });

    try {
      get().addConversationTurn({
        role: 'user',
        message: admitsUnknown ? `[I don't know] ${response}` : response,
        layer: 3,
        turn_number: get().conversationHistory.filter(t => t.layer === 3).length + 1,
      });

      const aiResponse = await feynmanService.respondWhySpiral({
        session_id: currentSession.session_id,
        response,
        admits_unknown: admitsUnknown,
      });

      if (aiResponse.next_question) {
        get().addConversationTurn({
          role: 'assistant',
          message: aiResponse.next_question,
          layer: 3,
          turn_number: get().conversationHistory.filter(t => t.layer === 3).length + 1,
        });
      } else if (aiResponse.boundary_detected) {
        get().addConversationTurn({
          role: 'assistant',
          message: `🎯 Knowledge boundary found: ${aiResponse.boundary_topic}\n\n${aiResponse.exploration_offer}`,
          layer: 3,
          turn_number: get().conversationHistory.filter(t => t.layer === 3).length + 1,
        });

        // Add gap
        if (aiResponse.boundary_topic) {
          set(state => ({
            discoveredGaps: [
              ...state.discoveredGaps,
              {
                gap_id: `temp-${Date.now()}`,
                topic: aiResponse.boundary_topic!,
                description: aiResponse.exploration_offer || '',
                layer_discovered: 3,
                why_depth: aiResponse.current_depth,
                resolved: false,
              },
            ],
          }));
        }
      }

      set({ whySpiralDepth: aiResponse.current_depth });

      // Move to layer 4 if boundary detected or reached max depth
      if (aiResponse.boundary_detected || aiResponse.current_depth >= 5) {
        set(state => ({
          currentSession: state.currentSession
            ? { ...state.currentSession, current_layer: 4 }
            : null,
        }));
      }

      set({ isLoading: false });
      return aiResponse;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 4: Submit analogy
  submitAnalogy: async (text, phase, defenseResponse) => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null, analogyPhase: phase });

    try {
      get().addConversationTurn({
        role: 'user',
        message: `[${phase}]: ${text}`,
        layer: 4,
        turn_number: get().conversationHistory.filter(t => t.layer === 4).length + 1,
      });

      const response = await feynmanService.submitAnalogy({
        session_id: currentSession.session_id,
        analogy_text: text,
        phase,
        defense_response: defenseResponse,
      });

      let feedbackMsg = `Score: ${response.score}/5\n`;
      feedbackMsg += `Strengths: ${response.strengths.join(', ')}\n`;
      feedbackMsg += `Weaknesses: ${response.weaknesses.join(', ')}`;
      if (response.stress_test_question) {
        feedbackMsg += `\n\n🔥 Stress Test: ${response.stress_test_question}`;
      }

      get().addConversationTurn({
        role: 'assistant',
        message: feedbackMsg,
        layer: 4,
        turn_number: get().conversationHistory.filter(t => t.layer === 4).length + 1,
      });

      // Move to layer 5 if analogy is good enough
      if (response.score >= 4 && phase === 'refine') {
        set(state => ({
          currentSession: state.currentSession
            ? { ...state.currentSession, current_layer: 5 }
            : null,
        }));
      }

      set({ isLoading: false });
      return response;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Layer 5: Teach Lecture Hall
  teachLectureHall: async (message) => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });

    try {
      get().addConversationTurn({
        role: 'user',
        message,
        layer: 5,
        turn_number: get().conversationHistory.filter(t => t.layer === 5).length + 1,
      });

      const response = await feynmanService.teachLectureHall({
        session_id: currentSession.session_id,
        message,
      });

      // Add each persona's response
      for (const persona of response.personas) {
        get().addConversationTurn({
          role: 'assistant',
          message: `[${persona.persona}]: ${persona.response}`,
          layer: 5,
          turn_number: get().conversationHistory.filter(t => t.layer === 5).length + 1,
        });
      }

      set({ lectureHallPersonas: response.personas, isLoading: false });
      return response;
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Complete session
  completeSession: async () => {
    const { currentSession } = get();
    if (!currentSession) throw new Error('No active session');

    set({ isLoading: true, error: null });

    try {
      await feynmanService.completeSession(currentSession.session_id);
      set(state => ({
        currentSession: state.currentSession
          ? { ...state.currentSession, status: 'completed' as any }
          : null,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
      throw error;
    }
  },

  // Reset state
  resetState: () => {
    set(initialState);
  },

  // Set error
  setError: (error) => {
    set({ error });
  },

  // Helper: Add conversation turn
  addConversationTurn: (turn) => {
    set(state => ({
      conversationHistory: [...state.conversationHistory, turn],
    }));
  },

  // Helper: Update Chintu metrics
  updateChintuMetrics: (confusion, curiosity) => {
    set({ chintuConfusion: confusion, chintuCuriosity: curiosity });
  },
}));
```

---

## 10. INTEGRATION POINTS

### 10.1 Future MCT Integration

The Feynman Engine is designed to integrate with MCT (Misconception Cascade Tracing) in the future:

```typescript
// In feynman_gaps.csv, there's a linked_session_id field
// This will link a Feynman gap to an MCT session

// Example integration flow:
// 1. Feynman discovers a gap
// 2. User clicks "Investigate this gap"
// 3. System creates an MCT session linked to this gap
// 4. MCT traces the root misconception
// 5. Resolution feeds back to mark the gap as resolved
```

### 10.2 Integration with Existing User System

```python
# The Feynman Engine uses the same user_id as the existing system
# XP earned should be added to the user's total XP in users.csv

# In the complete_session endpoint, add:
# user_service.add_xp(user_id, teaching_xp_earned)
```

### 10.3 Integration with Gamification

```python
# Teaching XP is separate from regular XP
# Consider adding to users.csv:
# teaching_xp, teaching_level

# Achievements earned should be stored in a user_achievements table
```

---

## 11. TESTING REQUIREMENTS

### 11.1 Backend Tests

Create `backend/tests/test_feynman.py`:

```python
"""
Tests for Feynman Engine
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_start_session():
    response = client.post("/api/feynman/session/start", json={
        "user_id": "test_user",
        "topic": "Photosynthesis",
        "subject": "Biology",
        "difficulty_level": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["topic"] == "Photosynthesis"


def test_teach_chintu():
    # First create a session
    session_response = client.post("/api/feynman/session/start", json={
        "user_id": "test_user",
        "topic": "Gravity",
        "subject": "Physics",
        "difficulty_level": 3
    })
    session_id = session_response.json()["session_id"]
    
    # Then teach Chintu
    response = client.post("/api/feynman/layer1/teach", json={
        "session_id": session_id,
        "message": "Gravity is like a magnet that pulls everything down to the ground.",
        "layer": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "confusion_level" in data
    assert 0 <= data["confusion_level"] <= 1


def test_compression_challenge():
    # Create session
    session_response = client.post("/api/feynman/session/start", json={
        "user_id": "test_user",
        "topic": "Electricity",
        "subject": "Physics"
    })
    session_id = session_response.json()["session_id"]
    
    # Submit compression
    response = client.post("/api/feynman/layer2/compress", json={
        "session_id": session_id,
        "word_limit": 100,
        "explanation": "Electricity is the flow of tiny particles called electrons through wires. When electrons move, they carry energy that can power our devices."
    })
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "passed" in data


def test_get_subjects():
    response = client.get("/api/feynman/subjects")
    assert response.status_code == 200
    data = response.json()
    assert "subjects" in data
    assert len(data["subjects"]) > 0
```

### 11.2 Frontend Tests

Create component tests using React Testing Library:

```typescript
// frontend/src/pages/FeynmanEngine/__tests__/ChintuMode.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChintuMode from '../ChintuMode';
import { useFeynmanStore } from '../../../store/feynmanStore';

// Mock the store
jest.mock('../../../store/feynmanStore');

describe('ChintuMode', () => {
  beforeEach(() => {
    (useFeynmanStore as jest.Mock).mockReturnValue({
      currentSession: {
        session_id: 'test-session',
        topic: 'Photosynthesis',
        subject: 'Biology',
      },
      conversationHistory: [],
      chintuConfusion: 0.5,
      chintuCuriosity: 0.5,
      isLoading: false,
      sendToChintu: jest.fn(),
    });
  });

  it('renders Chintu character', () => {
    render(<ChintuMode />);
    expect(screen.getByText(/Chintu/i)).toBeInTheDocument();
  });

  it('allows sending a message', async () => {
    const mockSendToChintu = jest.fn();
    (useFeynmanStore as jest.Mock).mockReturnValue({
      ...useFeynmanStore(),
      sendToChintu: mockSendToChintu,
    });

    render(<ChintuMode />);
    
    const input = screen.getByPlaceholderText(/explain/i);
    fireEvent.change(input, { target: { value: 'Plants make food using sunlight' } });
    
    const sendButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(mockSendToChintu).toHaveBeenCalledWith(
        'Plants make food using sunlight',
        undefined
      );
    });
  });
});
```

---

## IMPLEMENTATION CHECKLIST

### Phase 1: Backend Foundation
- [ ] Create all CSV files with headers
- [ ] Implement `feynman_models.py`
- [ ] Implement `feynman_db.py`
- [ ] Test database operations

### Phase 2: AI Service
- [ ] Implement `feynman_service.py`
- [ ] Test Chintu responses
- [ ] Test Compression evaluation
- [ ] Test Why Spiral
- [ ] Test Analogy evaluation
- [ ] Test Lecture Hall

### Phase 3: API Layer
- [ ] Implement `feynman.py` router
- [ ] Register router in main.py
- [ ] Test all endpoints with Postman/curl

### Phase 4: Frontend Foundation
- [ ] Create TypeScript types
- [ ] Implement API service
- [ ] Implement Zustand store

### Phase 5: Frontend UI
- [ ] Main FeynmanEngine page
- [ ] ChintuMode component
- [ ] CompressionMode component
- [ ] WhySpiralMode component
- [ ] AnalogyMode component
- [ ] LectureHallMode component
- [ ] Results/Summary component

### Phase 6: Integration & Testing
- [ ] Write backend tests
- [ ] Write frontend tests
- [ ] Integration testing
- [ ] Performance optimization

---

## FINAL NOTES

1. **Error Handling**: Always wrap AI calls in try-catch. The AI responses can be unpredictable.

2. **Rate Limiting**: Consider adding rate limiting to prevent API abuse.

3. **Caching**: Cache frequently requested data like subjects and topic suggestions.

4. **Logging**: Add comprehensive logging for debugging AI responses.

5. **Monitoring**: Track API response times and AI generation quality.

6. **Fallbacks**: Always have fallback responses if AI fails.

This specification should provide everything needed to implement the complete Feynman Engine feature. The implementation is modular, allowing for incremental development and testing.