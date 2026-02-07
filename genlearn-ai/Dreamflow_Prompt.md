# Mr. Feynmann - Dreamflow Build Prompt

> **App Name:** Mr. Feynmann  
> **Tagline:** "Teach me in your way"  
> **Platform:** Flutter (iOS & Android)  
> **Target:** Google Play Store & App Store  
> **Hackathon:** Dreamflow Hackathon - January 2026

---

## 🎯 PROJECT OVERVIEW

Build a Flutter mobile application called "Mr. Feynmann" that helps students learn through the Feynman Technique. The app has 3 main features:

1. **Feynman Technique** - Learn by teaching AI
2. **Mistake Autopsy** - Analyze and fix misconceptions  
3. **Dream Project** - Get personalized learning paths

The app uses **Google Gemini AI** for all AI interactions, **Hive** for local database storage, and **flutter_secure_storage** for managing API keys securely.

---

## 📦 DEPENDENCIES (pubspec.yaml)

```yaml
name: mr_feynmann
description: Learn by teaching - The Feynman Way
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # UI
  cupertino_icons: ^1.0.6
  google_fonts: ^6.1.0
  flutter_animate: ^4.3.0
  lottie: ^2.7.0
  
  # State Management
  provider: ^6.1.1
  
  # Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  flutter_secure_storage: ^9.0.0
  path_provider: ^2.1.1
  
  # AI
  google_generative_ai: ^0.4.0
  
  # Utilities
  uuid: ^4.2.1
  intl: ^0.18.1
  flutter_markdown: ^0.6.18
  
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  hive_generator: ^2.0.1
  build_runner: ^2.4.7

flutter:
  uses-material-design: true
  
  assets:
    - assets/images/
    - assets/animations/
```

---

## 📁 PROJECT STRUCTURE

```
lib/
├── main.dart
├── app.dart
├── config/
│   ├── theme.dart
│   ├── routes.dart
│   └── constants.dart
├── models/
│   ├── user.dart
│   ├── feynman_session.dart
│   ├── mct_session.dart
│   ├── dream_project.dart
│   └── chat_message.dart
├── services/
│   ├── gemini_service.dart
│   ├── storage_service.dart
│   ├── secure_storage_service.dart
│   └── hive_service.dart
├── providers/
│   ├── auth_provider.dart
│   ├── feynman_provider.dart
│   ├── mct_provider.dart
│   └── dream_provider.dart
├── screens/
│   ├── splash_screen.dart
│   ├── onboarding_screen.dart
│   ├── login_screen.dart
│   ├── register_screen.dart
│   ├── home_screen.dart
│   ├── feynman/
│   │   ├── feynman_home_screen.dart
│   │   ├── feynman_session_screen.dart
│   │   └── feynman_history_screen.dart
│   ├── mct/
│   │   ├── mct_home_screen.dart
│   │   ├── mct_session_screen.dart
│   │   └── mct_history_screen.dart
│   └── dream/
│       ├── dream_home_screen.dart
│       ├── dream_create_screen.dart
│       └── dream_roadmap_screen.dart
├── widgets/
│   ├── common/
│   │   ├── custom_button.dart
│   │   ├── custom_text_field.dart
│   │   ├── loading_widget.dart
│   │   ├── chat_bubble.dart
│   │   └── feature_card.dart
│   ├── feynman/
│   │   ├── layer_indicator.dart
│   │   └── teaching_prompt.dart
│   ├── mct/
│   │   ├── phase_indicator.dart
│   │   └── cascade_visualization.dart
│   └── dream/
│       ├── milestone_card.dart
│       └── roadmap_timeline.dart
└── utils/
    ├── validators.dart
    └── helpers.dart
```

---

## 🎨 THEME AND STYLING

### Color Palette
```dart
// Primary Colors
static const primaryBlue = Color(0xFF2563EB);
static const primaryPurple = Color(0xFF7C3AED);
static const primaryTeal = Color(0xFF0D9488);

// Accent Colors
static const accentOrange = Color(0xFFF97316);
static const accentPink = Color(0xFFEC4899);
static const accentGreen = Color(0xFF10B981);

// Background Colors
static const backgroundLight = Color(0xFFF8FAFC);
static const backgroundDark = Color(0xFF0F172A);
static const cardBackground = Color(0xFFFFFFFF);

// Text Colors
static const textPrimary = Color(0xFF1E293B);
static const textSecondary = Color(0xFF64748B);
static const textLight = Color(0xFFFFFFFF);

// Feature Colors
static const feynmanColor = Color(0xFF3B82F6);  // Blue
static const mctColor = Color(0xFFEF4444);       // Red
static const dreamColor = Color(0xFF8B5CF6);     // Purple
```

### Typography
- Use Google Fonts: **Outfit** for headings, **Inter** for body text
- Headings: Bold, sizes 32/28/24/20/18
- Body: Regular/Medium, sizes 16/14/12

### Design System
- Border radius: 16px for cards, 12px for buttons, 24px for inputs
- Shadows: Subtle elevation with blur 20, opacity 0.08
- Spacing: 8px base unit (8, 16, 24, 32, 48)
- Animations: Smooth 300ms transitions, spring physics for interactions

---

## 🔐 AUTHENTICATION (User Only - No Admin)

### Login Screen
- Email input field with validation
- Password input field with show/hide toggle
- "Remember Me" checkbox
- Login button with loading state
- "Forgot Password?" link (show coming soon dialog)
- "Create Account" link to register screen
- App logo and tagline at top

### Register Screen
- Name input field
- Email input field with validation
- Password input with strength indicator
- Confirm password field
- Terms and conditions checkbox
- Register button with loading state
- "Already have account?" link to login

### User Model (Hive)
```dart
@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)
  String name;
  
  @HiveField(2)
  String email;
  
  @HiveField(3)
  String passwordHash;
  
  @HiveField(4)
  DateTime createdAt;
  
  @HiveField(5)
  int totalXP;
  
  @HiveField(6)
  int currentStreak;
}
```

### Password Hashing
- Use simple SHA256 hash for password storage (no external auth needed)
- Store hashed password in Hive

---

## 🏠 HOME SCREEN

After login, show home screen with:

### Header
- "Hello, {userName}!" greeting
- Current XP badge
- Streak counter with fire icon

### 3 Feature Cards (Horizontal Scroll or Grid)

**Card 1: Feynman Technique** 🧠
- Icon: Brain with lightbulb
- Color: Blue gradient
- Tagline: "Learn by Teaching"
- Description: "Explain concepts to AI and discover gaps in your knowledge"

**Card 2: Mistake Autopsy** 🔬
- Icon: Magnifying glass with bug
- Color: Red gradient  
- Tagline: "Debug Your Brain"
- Description: "Trace your errors to their root cause"

**Card 3: Dream Project** 🚀
- Icon: Rocket
- Color: Purple gradient
- Tagline: "Build Your Dream"
- Description: "Get a personalized learning roadmap"

### Bottom Navigation
- Home (house icon)
- History (clock icon)
- Profile (person icon)

---

## 🧠 FEATURE 1: FEYNMAN TECHNIQUE

### How It Works
The Feynman Technique has 5 layers that progressively test understanding:

| Layer | Name | Challenge |
|-------|------|-----------|
| 1 | Create | Explain the topic in simple words |
| 2 | Defend | Answer challenger questions |
| 3 | Refine | Fill gaps with analogies |
| 4 | Stretch | Apply to new scenarios |
| 5 | Teach | Create teaching material |

### Feynman Home Screen
- Topic input field with suggestions
- Subject dropdown (Math, Science, History, etc.)
- "Start Learning" button
- Recent sessions list (click to resume)

### Feynman Session Screen
- Current layer indicator (1-5 dots, active one highlighted)
- Layer name and description
- Chat interface with:
  - AI question/prompt at top
  - User response input at bottom
  - Send button
- "Need Hint" button
- Progress bar showing layer completion

### AI Prompts for Each Layer

**Layer 1 - Create:**
```
You are a curious 10-year-old student. The user wants to teach you about {topic}. 
Ask them to explain it simply. If they use complex words, ask "What does that mean?"
Be genuinely curious and ask follow-up questions.
Keep responses short (2-3 sentences max).
```

**Layer 2 - Defend:**
```
You are now a skeptical student who questions everything about {topic}.
Challenge the user's explanation with "But why?" and "How do you know?"
Point out logical gaps gently. Keep responses short.
```

**Layer 3 - Refine:**
```
You are an analogy expert. Ask the user to explain {topic} using a real-world analogy.
If their analogy has flaws, point them out. Help them refine it.
```

**Layer 4 - Stretch:**
```
You are a practical thinker. Present a new scenario where {topic} applies.
Ask the user how the concept works in this new context.
Test if they can transfer their knowledge.
```

**Layer 5 - Teach:**
```
You are now the student's assistant. Ask them to create a short teaching summary 
about {topic} that would help another student understand.
Evaluate if it's clear and complete.
```

### Session Model (Hive)
```dart
@HiveType(typeId: 1)
class FeynmanSession extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)
  String topic;
  
  @HiveField(2)
  String subject;
  
  @HiveField(3)
  int currentLayer; // 1-5
  
  @HiveField(4)
  List<ChatMessage> messages;
  
  @HiveField(5)
  DateTime createdAt;
  
  @HiveField(6)
  DateTime? completedAt;
  
  @HiveField(7)
  int score; // 0-100
}
```

### Scoring
- Each layer: 20 points max
- AI evaluates responses and gives partial credit
- Total score out of 100
- Award XP based on score

---

## 🔬 FEATURE 2: MISTAKE AUTOPSY (MCT)

### How It Works
Misconception Cascade Tracing (MCT) uses 5 phases to trace errors to their root:

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | Surface Capture | Identify the visible error |
| 2 | Diagnostic Probing | Ask targeted questions |
| 3 | Root Found | Identify fundamental misconception |
| 4 | Remediation | Repair the broken concept |
| 5 | Verification | Confirm understanding |

### MCT Home Screen
- "What was the question?" input
- "Your answer" input
- "Correct answer" input
- Subject dropdown
- "Start Autopsy" button
- OR "Load from History" to analyze past sessions

### MCT Session Screen
- Phase indicator (5 colored dots)
- Current phase name with icon
- Chat interface
- Phase-specific cards showing:
  - Surface error identified
  - Tested prerequisites
  - Root misconception (when found)
  - Repair progress

### AI Prompts for MCT

**System Prompt:**
```
You are Dr. Feynman, a diagnostic educator. Your job is to trace why a student made a mistake.

Question: {question}
Student's Answer: {student_answer}
Correct Answer: {correct_answer}
Subject: {subject}

Use the Socratic method. Ask ONE probing question at a time.
Never give answers directly - guide them to discover their own errors.
Keep responses under 3 sentences.

Track the cascade:
- What surface error did they make?
- What prerequisite knowledge might be missing?
- What is the root misconception?

Current Phase: {phase}
Conversation History: {history}
```

**Phase-Specific Behavior:**
- Phase 1: Identify what type of error (conceptual, procedural, careless)
- Phase 2: Ask "Why did you think...?" questions
- Phase 3: Name the root misconception when found
- Phase 4: Explain the correct concept simply
- Phase 5: Give a verification question

### MCT Session Model (Hive)
```dart
@HiveType(typeId: 2)
class MCTSession extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)
  String question;
  
  @HiveField(2)
  String studentAnswer;
  
  @HiveField(3)
  String correctAnswer;
  
  @HiveField(4)
  String subject;
  
  @HiveField(5)
  String currentPhase; // surface_capture, diagnostic_probing, root_found, remediation, verification
  
  @HiveField(6)
  List<ChatMessage> messages;
  
  @HiveField(7)
  String? rootMisconception;
  
  @HiveField(8)
  DateTime createdAt;
  
  @HiveField(9)
  bool isCompleted;
}
```

---

## 🚀 FEATURE 3: DREAM PROJECT

### How It Works
User describes their dream project, AI creates a personalized learning roadmap.

### Dream Home Screen
- Inspirational header "What do you want to build?"
- Large text input for dream description
- Example dreams as chips:
  - "Build a mobile app"
  - "Create a video game"
  - "Make a robot"
  - "Write a novel"
  - "Start a YouTube channel"
- "Create My Roadmap" button
- Saved projects list

### Dream Create Screen
- Dream description input (multiline)
- "How many hours per week?" slider (1-20)
- "What's your experience level?" (Beginner/Intermediate/Advanced)
- "Generate Roadmap" button with loading animation

### Dream Roadmap Screen
- Project name at top
- Timeline visualization (vertical)
- Milestones as cards:
  - Week number
  - Milestone title
  - Key skills to learn
  - Mini tasks (checkboxes)
  - Estimated hours
- Progress bar overall
- "Start Learning" button on each milestone

### AI Prompt for Dream Project
```
You are a career mentor and learning path designer. 
Create a personalized learning roadmap for someone who wants to: {dream}

Their details:
- Hours available per week: {hours}
- Current level: {level}

Create a roadmap with 6-10 milestones. For each milestone provide:
1. Week number (when to start)
2. Milestone name
3. 3-5 key skills to learn
4. 3-5 specific tasks
5. Estimated hours
6. Free resources (websites, YouTube channels, books)

Format as JSON:
{
  "projectName": "...",
  "totalWeeks": N,
  "milestones": [
    {
      "week": 1,
      "name": "...",
      "skills": ["...", "..."],
      "tasks": ["...", "..."],
      "hours": N,
      "resources": ["...", "..."]
    }
  ]
}
```

### Dream Project Model (Hive)
```dart
@HiveType(typeId: 3)
class DreamProject extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)
  String dream;
  
  @HiveField(2)
  String projectName;
  
  @HiveField(3)
  int hoursPerWeek;
  
  @HiveField(4)
  String level;
  
  @HiveField(5)
  List<Milestone> milestones;
  
  @HiveField(6)
  int currentMilestone;
  
  @HiveField(7)
  DateTime createdAt;
  
  @HiveField(8)
  int completedTasks;
  
  @HiveField(9)
  int totalTasks;
}

@HiveType(typeId: 4)
class Milestone extends HiveObject {
  @HiveField(0)
  int week;
  
  @HiveField(1)
  String name;
  
  @HiveField(2)
  List<String> skills;
  
  @HiveField(3)
  List<Task> tasks;
  
  @HiveField(4)
  int hours;
  
  @HiveField(5)
  List<String> resources;
  
  @HiveField(6)
  bool isCompleted;
}
```

---

## 💬 CHAT MESSAGE MODEL (Shared)

```dart
@HiveType(typeId: 5)
class ChatMessage extends HiveObject {
  @HiveField(0)
  String id;
  
  @HiveField(1)
  String role; // 'user' or 'assistant'
  
  @HiveField(2)
  String content;
  
  @HiveField(3)
  DateTime timestamp;
  
  @HiveField(4)
  String? phase; // For MCT
  
  @HiveField(5)
  int? layer; // For Feynman
}
```

---

## 🔑 SECURE STORAGE SERVICE

Store API keys securely using flutter_secure_storage:

```dart
class SecureStorageService {
  final _storage = FlutterSecureStorage();
  
  // Keys
  static const _geminiApiKey = 'gemini_api_key';
  static const _userToken = 'user_token';
  
  Future<void> saveGeminiApiKey(String key) async {
    await _storage.write(key: _geminiApiKey, value: key);
  }
  
  Future<String?> getGeminiApiKey() async {
    return await _storage.read(key: _geminiApiKey);
  }
  
  Future<void> saveUserToken(String token) async {
    await _storage.write(key: _userToken, value: token);
  }
  
  Future<String?> getUserToken() async {
    return await _storage.read(key: _userToken);
  }
  
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
```

---

## 🤖 GEMINI SERVICE

```dart
class GeminiService {
  GenerativeModel? _model;
  final SecureStorageService _secureStorage;
  
  GeminiService(this._secureStorage);
  
  Future<void> initialize() async {
    final apiKey = await _secureStorage.getGeminiApiKey();
    if (apiKey != null && apiKey.isNotEmpty) {
      _model = GenerativeModel(
        model: 'gemini-1.5-flash',
        apiKey: apiKey,
      );
    }
  }
  
  Future<String> chat(String systemPrompt, List<ChatMessage> history, String userMessage) async {
    if (_model == null) {
      throw Exception('Gemini not initialized. Please add API key in settings.');
    }
    
    // Build conversation
    final messages = [
      Content.text(systemPrompt),
      ...history.map((m) => Content.text('${m.role}: ${m.content}')),
      Content.text('user: $userMessage'),
    ];
    
    final response = await _model!.generateContent(messages);
    return response.text ?? 'I could not generate a response.';
  }
  
  Future<Map<String, dynamic>> generateRoadmap(String prompt) async {
    if (_model == null) {
      throw Exception('Gemini not initialized.');
    }
    
    final response = await _model!.generateContent([Content.text(prompt)]);
    final text = response.text ?? '{}';
    
    // Parse JSON from response
    final jsonMatch = RegExp(r'\{[\s\S]*\}').firstMatch(text);
    if (jsonMatch != null) {
      return jsonDecode(jsonMatch.group(0)!);
    }
    throw Exception('Could not parse roadmap');
  }
}
```

---

## 💾 HIVE SERVICE

```dart
class HiveService {
  static Future<void> initialize() async {
    await Hive.initFlutter();
    
    // Register adapters
    Hive.registerAdapter(UserAdapter());
    Hive.registerAdapter(FeynmanSessionAdapter());
    Hive.registerAdapter(MCTSessionAdapter());
    Hive.registerAdapter(DreamProjectAdapter());
    Hive.registerAdapter(MilestoneAdapter());
    Hive.registerAdapter(ChatMessageAdapter());
    
    // Open boxes
    await Hive.openBox<User>('users');
    await Hive.openBox<FeynmanSession>('feynman_sessions');
    await Hive.openBox<MCTSession>('mct_sessions');
    await Hive.openBox<DreamProject>('dream_projects');
  }
  
  // User operations
  Box<User> get userBox => Hive.box<User>('users');
  
  User? getCurrentUser() {
    return userBox.get('current_user');
  }
  
  Future<void> saveUser(User user) async {
    await userBox.put('current_user', user);
    await userBox.put(user.id, user);
  }
  
  // Feynman operations
  Box<FeynmanSession> get feynmanBox => Hive.box<FeynmanSession>('feynman_sessions');
  
  List<FeynmanSession> getFeynmanSessions() {
    return feynmanBox.values.toList()
      ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
  }
  
  // Similar methods for MCT and Dream...
}
```

---

## ⚙️ SETTINGS SCREEN

### Settings Options
- **Profile Section**
  - Name (editable)
  - Email (read-only)
  - Change Password
  
- **API Configuration**
  - Gemini API Key input (masked, with show/hide)
  - "Test Connection" button
  - Status indicator (Connected/Not Connected)
  
- **App Settings**
  - Dark Mode toggle
  - Notifications toggle
  
- **Data**
  - Export Data button
  - Clear All Data button (with confirmation)
  
- **About**
  - App version
  - Credits
  - Privacy Policy link

---

## 🚀 MAIN.DART

```dart
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive
  await HiveService.initialize();
  
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => FeynmanProvider()),
        ChangeNotifierProvider(create: (_) => MCTProvider()),
        ChangeNotifierProvider(create: (_) => DreamProvider()),
      ],
      child: const MrFeynmannApp(),
    ),
  );
}

class MrFeynmannApp extends StatelessWidget {
  const MrFeynmannApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mr. Feynmann',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      home: const SplashScreen(),
      routes: AppRoutes.routes,
    );
  }
}
```

---

## 📱 APP FLOW

```
1. Splash Screen (2 seconds, logo animation)
      ↓
2. Check if user logged in (Hive)
      ↓
   ┌─ Yes ─→ Home Screen
   └─ No ──→ Onboarding (3 slides) → Login/Register
      
3. Home Screen
   ├─ Feynman Card → Feynman Home → Session → Results
   ├─ MCT Card → MCT Home → Session → Root Found → Remediation
   └─ Dream Card → Dream Home → Create → Roadmap → Track Progress

4. Bottom Navigation
   ├─ Home (feature cards)
   ├─ History (all past sessions, filterable)
   └─ Profile (settings, stats, logout)
```

---

## ✅ CRITICAL IMPLEMENTATION NOTES

1. **API Key Setup**: On first launch, show a setup screen asking for Gemini API key. Store in flutter_secure_storage. Without it, AI features won't work.

2. **Offline Handling**: Show appropriate messages when offline. Hive data persists offline, but AI features need internet.

3. **Error Handling**: Wrap all Gemini calls in try-catch. Show user-friendly error messages.

4. **Loading States**: Every AI call should show a loading indicator. Use shimmer effects for better UX.

5. **Session Resume**: Users can resume incomplete Feynman/MCT sessions from history.

6. **XP System**: Award XP for:
   - Completing Feynman layer: 20 XP each
   - Completing MCT session: 50 XP
   - Creating Dream roadmap: 30 XP
   - Completing milestone task: 10 XP

7. **Streak Tracking**: Track daily usage. Show streak in home screen header.

8. **No Backend Required**: Everything runs locally with Hive. Only external call is to Gemini API.

---

## 🎯 BUILD CHECKLIST

- [ ] Splash screen with logo animation
- [ ] Onboarding (3 slides explaining features)
- [ ] Login/Register with local Hive storage
- [ ] Home screen with 3 feature cards
- [ ] Feynman Technique with 5-layer progression
- [ ] MCT with 5-phase diagnostic
- [ ] Dream Project with roadmap generation
- [ ] History screen with all sessions
- [ ] Profile/Settings screen
- [ ] API key configuration
- [ ] Dark mode support
- [ ] Loading states and error handling
- [ ] XP and streak tracking

---

## 📦 ASSETS NEEDED

Create these folders and add placeholder assets:

```
assets/
├── images/
│   ├── logo.png (App logo - brain with graduation cap)
│   ├── onboarding_1.png (Person teaching concept)
│   ├── onboarding_2.png (Debugging brain)
│   └── onboarding_3.png (Rocket launching)
└── animations/
    ├── loading.json (Lottie loading animation)
    ├── success.json (Lottie success checkmark)
    └── thinking.json (Lottie brain thinking)
```

---

## 🏁 FINAL NOTES

This app should feel:
- **Inspiring** - Help users believe they can learn anything
- **Simple** - Easy to understand and use
- **Engaging** - Gamification keeps users coming back
- **Smart** - AI responses feel helpful and personalized

Remember: The tagline is "Teach me in your way" - make the AI feel like a genuine learning companion, not a cold chatbot.


