# GenLearn AI - Quick Start Guide

## Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- GCP credentials configured (run `gcloud auth application-default login`)

---

## Start Backend

```bash
cd genlearn-ai/backend
py run.py
```

Or with auto-reload for development:
```bash
py run.py --reload
```

**Backend runs at:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

---

## Start Frontend

```bash
cd genlearn-ai/frontend
#npm install    # First time only
npm run dev
```

**Frontend runs at:** http://localhost:5173

---

## Login Credentials

| Username | Password | Role |
|----------|----------|------|
| DebK | password123 | User |
| admin | password123 | Admin |

---

## Troubleshooting

### Port already in use
```powershell
# Kill Python processes
Get-Process -Name python* | Stop-Process -Force
```

### GCP credentials error
```bash
gcloud auth application-default login
```
