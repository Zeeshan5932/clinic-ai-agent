# Clinic AI Receptionist Agent

A production-ready AI receptionist for clinics and aesthetic centers. Built with a modern, scalable monorepo structure separating frontend and backend.

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- FastAPI
- LangChain & LangGraph
- Groq LLM (with easy switching to other providers)
- PostgreSQL / SQLite
- SQLAlchemy ORM
- Pydantic for data validation

**Infrastructure:**
- Docker & docker-compose
- Environment-based configuration

## ✨ Features

- **AI-Powered Appointment Management**: Book, reschedule, and cancel appointments
- **FAQ System**: Answer clinic FAQs using LLM
- **Intent Detection**: Automatically detects user intent and routes to the appropriate handler
- **Modular Architecture**: Clean separation between API routes, business logic, and database layers
- **Type Safety**: Full TypeScript-style type hints with Pydantic
- **Comprehensive API**: RESTful endpoints for chat and appointment management
- **Production Ready**: Environment variables, logging, error handling, health checks

## 📁 Project Structure

```
clinic-ai-agent/
├── backend/                          # Backend Python FastAPI application
│   ├── app/
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── agent/                    # LangGraph AI agent
│   │   │   ├── graph.py              # Workflow graph definition
│   │   │   ├── nodes.py              # Node implementations
│   │   │   ├── prompts.py            # LLM prompts
│   │   │   ├── router.py             # Intent routing logic
│   │   │   └── state.py              # TypedDict state schema
│   │   ├── api/
│   │   │   └── routes/               # API route handlers
│   │   │       ├── chat.py           # Chat endpoint
│   │   │       ├── appointments.py   # Appointments CRUD
│   │   │       └── health.py         # Health check
│   │   ├── core/                     # Core functionality
│   │   │   ├── config.py             # Settings from env vars
│   │   │   ├── logging.py            # Logging setup
│   │   │   └── security.py           # Security utilities
│   │   ├── db/                       # Database layer
│   │   │   ├── database.py           # SQLAlchemy setup
│   │   │   └── models.py             # ORM models
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── chat.py               # Chat request/response
│   │   │   ├── appointment.py        # Appointment schemas
│   │   │   └── common.py             # Common schemas
│   │   ├── services/                 # Business logic
│   │   │   ├── llm_service.py        # LLM provider (Groq)
│   │   │   ├── calendar_service.py   # Calendar integration
│   │   │   └── email_service.py      # Email integration
│   │   ├── tools/                    # Agent tools
│   │   │   ├── booking_tool.py
│   │   │   ├── reschedule_tool.py
│   │   │   ├── cancel_tool.py
│   │   │   ├── faq_tool.py
│   │   │   └── email_tool.py
│   │   └── utils/                    # Utility functions
│   │       ├── helpers.py
│   │       ├── validators.py
│   │       └── datetime_utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── tests/
│
├── frontend/                         # Frontend (placeholder)
│   └── README.md                     # Frontend setup instructions
│
├── docker-compose.yml                # Monorepo docker setup
├── .gitignore
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker & docker-compose (recommended)
- Python 3.11+ (for local development)
- Groq API key (get free at https://console.groq.com)
- python -m uvicorn app.main:app --reload
### Option 1: Run with Docker (Recommended)

```bash
# Clone the repo
git clone <repo-url> clinic-ai-agent
cd clinic-ai-agent

# Create backend .env from example
cp backend/.env.example backend/.env

# Edit backend/.env and add your GROQ_API_KEY
# nano backend/.env

# Start services
docker-compose up --build

# API available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### Option 2: Local Development

**Backend Setup:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# For local SQLite (default), just run:
uvicorn app.main:app --reload

# For PostgreSQL, set DATABASE_URL and run postgres separately
```

**Access the API:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health
- Chat: POST http://localhost:8000/api/v1/chat

## 📖 API Endpoints

### Chat (AI Agent)
```bash
POST /api/v1/chat
Content-Type: application/json

{
  "message": "I want to book an appointment for a facial next Monday at 3pm"
}

# Response:
{
  "response": "Appointment booked for ..."
}
```

### Appointments (Manage Bookings)
```bash
# List appointments
GET /api/v1/appointments

# Get specific appointment
GET /api/v1/appointments/{id}

# Create appointment
POST /api/v1/appointments
{
  "patient_name": "John Doe",
  "service": "Facial",
  "scheduled_time": "2026-03-28T15:00:00"
}

# Update appointment
PUT /api/v1/appointments/{id}
{
  "scheduled_time": "2026-03-29T14:00:00"
}

# Cancel appointment
DELETE /api/v1/appointments/{id}
```

### Health Check
```bash
GET /api/v1/health
# Response: { "status": "healthy", "message": "..." }
```

## 🔧 Environment Variables

**Required:**
- `GROQ_API_KEY` - Your Groq API key

**Optional but Recommended:**
- `APP_ENV` - development, staging, production
- `DEBUG` - true/false for debug logging
- `DATABASE_URL` - SQLite (default) or PostgreSQL connection string
- `GROQ_MODEL` - Model ID (default: llama-3.3-70b-versatile)
- `SECRET_KEY` - JWT secret (change in production)

**Clinic Information** (for FAQ system):
- `CLINIC_NAME`
- `CLINIC_EMAIL`
- `CLINIC_PHONE`
- `CLINIC_ADDRESS`
- `CLINIC_WORKING_HOURS`

[See `backend/.env.example` for full list]

## 🤖 How It Works

1. **User sends a message** → POST /api/v1/chat
2. **Intent detection** → LLM identifies: booking, reschedule, cancel, or faq
3. **Conditional routing** → LangGraph routes to appropriate handler
4. **Detail extraction** → LLM extracts structured data (patient name, date, etc.)
5. **Action execution** → Handler (booking/reschedule/cancel) updates database
6. **Response** → Summary sent back to user

### AI Agent Workflow

```
Input Message
    ↓
[Detect Intent] ← LLM
    ↓
┌─────────────────────────────────────────┐
│  Route based on intent:                 │
├─────────────────────────────────────────┤
│  booking → [Extract Details] → BookDB   │
│  reschedule → [Extract Details] → UpdateDB │
│  cancel → [Extract Details] → CancelDB  │
│  faq → [Answer via LLM]                 │
└─────────────────────────────────────────┘
    ↓
Response to User
```

## 🔄 Switching LLM Providers

The project uses abstracted LLM through `backend/app/services/llm_service.py`.

**To switch from Groq to another provider:**

1. Edit `backend/app/services/llm_service.py`
2. Replace ChatGroq with your provider (e.g., ChatOpenAI, ChatAnthropic)
3. Update environment variables
4. Update `backend/requirements.txt` with new dependencies

```python
# Example: Switch to OpenAI
from langchain_openai import ChatOpenAI
def get_llm():
    return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")
```

## 📝 Database

**Default:** SQLite (local dev)
```bash
# Database file created at: clinic.db
```

**Production:** PostgreSQL

Update `backend/.env`:
```
DATABASE_URL=postgresql://user:password@postgres:5432/clinicdb
```

Docker-compose automatically includes Postgres service when using `docker-compose up`.

## 🧪 Testing

```bash
cd backend
pytest tests/
```

## 📚 Project Features Breakdown

| Feature | Status | Notes |
|---------|--------|-------|
| Appointment Booking | ✅ | Via LLM + database |
| Appointment Rescheduling | ✅ | Via agent |
| Appointment Cancellation | ✅ | Via agent |
| FAQ System | ✅ | LLM-powered responses |
| REST API | ✅ | Full CRUD for appointments |
| Health Checks | ✅ | /api/v1/health |
| Logging | ✅ | Structured logs |
| Error Handling | ✅ | Proper HTTP status codes |
| Docker Support | ✅ | Compose file included |
| Type Safety | ✅ | Pydantic models |
| Modular Design | ✅ | Clean separation of concerns |

## 🔐 Security Notes

- **Production deployment**: Change `SECRET_KEY` in .env
- **CORS**: Update allowed origins in `backend/app/main.py`
- **API Rate Limiting**: Consider adding rate limiting middleware
- **Authentication**: Add JWT tokens if needed
- **Secrets Management**: Never commit .env files

## 📄 License

This project is provided as-is for clinic and healthcare professionals.

## 🤝 Support

For issues, questions, or contributions, please create an issue or pull request.

---

**Happy scheduling!** 🏥

