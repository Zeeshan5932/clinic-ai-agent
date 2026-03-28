# Migration Guide: Refactored to Monorepo Structure

This document explains the changes made during the refactoring and how to use the new structure.

## What Changed?

### ✨ New Structure

The project has been refactored from a single `app/` folder at the root into a production-grade monorepo with `backend/` and `frontend/` folders.

**Old Structure:**
```
clinic-ai-agent/
├── app/
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

**New Structure:**
```
clinic-ai-agent/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   └── README.md
├── docker-compose.yml
├── .gitignore
└── README.md
```

### 🔄 Groq Integration

- **Before**: Used OpenAI (GPT-4o)
- **After**: Uses Groq (llama-3.3-70b-versatile)

All LLM calls now go through `backend/app/services/llm_service.py`, making it easy to switch providers.

### 📦 Backend Reorganization

**New folder structure for backend:**

```
backend/app/
├── agent/          # LangGraph workflow
├── api/routes/     # API endpoints (chat, appointments, health)
├── core/           # Config, logging, security
├── db/             # Database models and setup
├── schemas/        # Pydantic request/response models
├── services/       # Business logic (LLM, calendar, email)
├── tools/          # Agent tools (booking, reschedule, etc.)
└── utils/          # Helpers, validators, datetime utils
```

### 🎯 Key Improvements

1. **Separation of Concerns**
   - API routes isolated in `api/routes/`
   - Business logic in `services/`
   - Database layer separated in `db/`
   - Pydantic schemas in `schemas/`

2. **Configuration**
   - New `core/config.py` loads from `backend/.env`
   - Support for 20+ environment variables
   - Better defaults for local development

3. **LLM Flexibility**
   - New `services/llm_service.py` abstracts LLM provider
   - Easy to switch from Groq to OpenAI, Claude, etc.
   - Uses LangChain's Chat interfaces

4. **API Improvements**
   - Multiple endpoints: chat, appointments, health
   - Proper REST conventions
   - Type-safe request/response schemas
   - Better error handling

5. **Development Quality**
   - Comprehensive logging
   - Health checks
   - Database migrations ready
   - Test directory for future tests

## 🚀 How to Run

### Quick Start (Docker)

```bash
# Clone and navigate
git clone <repo> clinic-ai-agent
cd clinic-ai-agent

# Setup backend environment
cp backend/.env.example backend/.env

# Edit backend/.env and add:
# GROQ_API_KEY=your_key_here

# Run with Docker
docker-compose up --build
```

Access at: `http://localhost:8000`

### Local Development (Without Docker)

**Backend only:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Edit .env and add GROQ_API_KEY

# Run
uvicorn app.main:app --reload
```

**Access:**
- Docs: http://localhost:8000/docs
- Chat: POST http://localhost:8000/api/v1/chat
- Health: GET http://localhost:8000/api/v1/health

## 📝 Environment Variables

The new `backend/.env.example` includes:

```bash
# Required
GROQ_API_KEY=your_groq_api_key

# App Configuration
APP_NAME="Clinic AI Receptionist"
APP_ENV=development
DEBUG=true

# Database (default: SQLite for local dev)
DATABASE_URL=sqlite:///./clinic.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@postgres:5432/clinicdb

# API
API_HOST=0.0.0.0
API_PORT=8000

# ... and 10+ more optional variables
```

See `backend/.env.example` for complete list.

## 🔄 Upgrading From Old Version

If you have an existing `.env` file with `OPENAI_API_KEY`:

1. **Backup your old .env**
   ```bash
   cp .env .env.backup
   ```

2. **Create new backend .env**
   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Update to Groq**
   - Get Groq API key from https://console.groq.com
   - Add to `backend/.env`:
     ```
     GROQ_API_KEY=your_groq_key_here
     ```

4. **If using PostgreSQL**
   - Update DATABASE_URL in `backend/.env`

5. **Run**
   ```bash
   docker-compose up --build
   # or locally:
   cd backend && uvicorn app.main:app --reload
   ```

## 📚 API Changes

### New Endpoints

All endpoints now have `/api/v1/` prefix:

**Chat**
- `POST /api/v1/chat` (same as before, but new path)

**Appointments (NEW!)**
- `GET /api/v1/appointments` - List all
- `GET /api/v1/appointments/{id}` - Get one
- `POST /api/v1/appointments` - Create
- `PUT /api/v1/appointments/{id}` - Update
- `DELETE /api/v1/appointments/{id}` - Cancel

**Health (NEW!)**
- `GET /api/v1/health` - Check API status

### Documentation

Interactive API docs automatically available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI spec: http://localhost:8000/openapi.json

## 🗄️ Database

### Local Development
- **Default**: SQLite (no setup needed)
- File created at: `backend/clinic.db`

### Production
- **Recommended**: PostgreSQL
- Update `DATABASE_URL` in `backend/.env`
- Docker-compose includes Postgres service

### Schema
- Appointments table with columns:
  - id, patient_name, service, scheduled_time, status, created_at, updated_at

## 🔧 Common Tasks

### Change LLM Provider

Edit `backend/app/services/llm_service.py`:

```python
# From Groq
from langchain_groq import ChatGroq
def get_llm():
    return ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL)

# To OpenAI
from langchain_openai import ChatOpenAI
def get_llm():
    return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")

# To Anthropic
from langchain_anthropic import ChatAnthropic
def get_llm():
    return ChatAnthropic(api_key=settings.ANTHROPIC_API_KEY, model="claude-3-opus")
```

### Run Tests
```bash
cd backend
pytest tests/
```

### Generate API Documentation
```bash
# Already auto-generated at /docs and /redoc
# To export OpenAPI spec:
curl http://localhost:8000/openapi.json > openapi.json
```

### Debug Mode
```bash
# Enable in backend/.env
DEBUG=true

# Or run:
cd backend && uvicorn app.main:app --reload --log-level debug
```

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

```bash
# Make sure you're in the backend directory:
cd backend
uvicorn app.main:app --reload

# Not from the root!
```

### "GROQ_API_KEY not set"

```bash
# Check backend/.env exists and has GROQ_API_KEY
cat backend/.env | grep GROQ_API_KEY

# Or set as environment variable:
export GROQ_API_KEY=your_key_here
```

### Port 8000 Already in Use

```bash
# Use a different port:
cd backend && uvicorn app.main:app --port 8001

# Or kill existing process:
# Linux/Mac: lsof -i :8000 | kill -9 <PID>
# Windows: netstat -ano | findstr :8000 then taskkill /PID <PID>
```

### Database Errors

```bash
# Reset SQLite database:
cd backend && rm clinic.db

# Then run - database will recreate:
uvicorn app.main:app --reload
```

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Groq API Documentation](https://console.groq.com/docs)

## ✅ Checklist for First Run

- [ ] Clone repo
- [ ] Create `backend/.env` from `.env.example`
- [ ] Add `GROQ_API_KEY` to `backend/.env`
- [ ] Run `docker-compose up --build` OR `cd backend && uvicorn app.main:app --reload`
- [ ] Test chat at http://localhost:8000/api/v1/chat
- [ ] View docs at http://localhost:8000/docs
- [ ] Create an appointment via API

## 🎉 You're All Set!

The refactored project is production-ready with:
- ✅ Clean monorepo structure
- ✅ Groq LLM integration
- ✅ Full RESTful API
- ✅ Type-safe schemas
- ✅ Comprehensive configuration
- ✅ Docker support
- ✅ Health checks & logging

Happy building! 🚀
