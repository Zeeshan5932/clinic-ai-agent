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
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── components/               # Reusable UI components
│   │   ├── pages/                    # Route pages (Home, Chat, FAQ, Appointments)
│   │   ├── services/                 # API client layer
│   │   ├── hooks/                    # Custom React hooks
│   │   └── utils/                    # Frontend utility helpers
│   ├── public/
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
### Option 1: Run with Docker (Recommended)

```bash
# Clone the repo
git clone <repo-url> clinic-ai-agent
cd clinic-ai-agent

# Create root .env from backend template
cp backend/.env.example .env

# Edit .env and add your GROQ_API_KEY

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

# Create or update root .env (preferred)
cd ..
cp backend/.env.example .env
# Edit .env and add your GROQ_API_KEY
cd backend

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

1. **User interacts in UI** (Chat page or quick action)
2. **Frontend API layer** sends request to backend `/api/v1/chat`
3. **LangGraph detect-intent node** classifies message into booking/reschedule/cancel/faq
4. **Router selects tool path** and runs the correct node
5. **Tool executes business action**:
   - booking/reschedule/cancel: updates SQLAlchemy database
   - faq: gets answer from Groq through LangChain
6. **Response is returned** to frontend and rendered in chat messages
7. **Optional side effects** (email/calendar) are triggered by service layer

### End-to-End Visual Flow

```mermaid
flowchart TD
  A[Patient Message in React UI] --> B[POST /api/v1/chat]
  B --> C[FastAPI Chat Route]
  C --> D[LangGraph Agent]
  D --> E[Detect Intent Node]
  E -->|booking| F[Booking Node]
  E -->|reschedule| G[Reschedule Node]
  E -->|cancel| H[Cancel Node]
  E -->|faq| I[FAQ Node]

  F --> J[(Appointments DB)]
  G --> J
  H --> J
  I --> K[Groq LLM]

  F --> L[Optional Calendar/Email Service]
  G --> L
  H --> L

  J --> M[Structured Agent Response]
  K --> M
  L --> M
  M --> N[Frontend Chat UI Update]
```

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

## 🎯 Next Aim: Twilio + WhatsApp Integration

The next milestone is to make this receptionist available on phone/SMS/WhatsApp in addition to the web app.

### Target Flow

1. Patient sends WhatsApp or SMS message to Twilio number.
2. Twilio webhook calls backend endpoint (example: `POST /api/v1/channels/twilio/webhook`).
3. Backend maps message into existing LangGraph chat input.
4. Agent generates response using same booking/faq logic.
5. Backend sends reply back through Twilio API.

### Implementation Plan

1. **Add channel webhook route**
  - New route module: `backend/app/api/routes/channels.py`
  - Validate Twilio signature for security.
2. **Add Twilio service layer**
  - New service: `backend/app/services/twilio_service.py`
  - Handle send/receive message helpers.
3. **Reuse existing agent graph**
  - No duplicate business logic.
  - Convert Twilio payload to `ChatRequest` style input.
4. **Persist channel metadata**
  - Store sender phone, channel type, and conversation IDs for audit/history.
5. **Add outbound templates**
  - Appointment confirmation, reminder, cancellation, and reschedule messages.

### Required Env Vars for Twilio

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_WHATSAPP_NUMBER` (example: `whatsapp:+14155238886`)
- `TWILIO_WEBHOOK_BASE_URL`

## 📝 Database

**Default:** SQLite (local dev)
```bash
# Database file created at: clinic.db
```

**Production:** PostgreSQL

Update root `.env`:
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

