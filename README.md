# Clinic AI Receptionist Agent

A production-ready AI receptionist for clinics and aesthetic centers, built with:

- Python 3.11
- FastAPI
- LangChain & LangGraph
- OpenAI GPT-4o
- PostgreSQL with SQLAlchemy
- Docker / docker-compose

## Features

- Appointment booking, rescheduling, cancellation
- FAQ answering about services, pricing, hours, and location
- Modular architecture with clear separation of concerns
- Workflow control via LangGraph with typed state schema
- Environment variable configuration

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url> clinic-ai-agent
   cd clinic-ai-agent
   ```

2. **Copy environment example**
   ```bash
   cp .env.example .env
   # then fill in your OpenAI key and other settings
   ```

3. **Install dependencies (optional, when running locally)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

4. **Run with Docker**
   Make sure you have Docker and docker-compose installed.
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

## Environment Variables

| Name            | Description                               |
|-----------------|-------------------------------------------|
| OPENAI_API_KEY  | Your OpenAI API key                       |
| DATABASE_URL    | SQLAlchemy connection string for Postgres |
| API_HOST        | Host for FastAPI (default: 0.0.0.0)       |
| API_PORT        | Port for FastAPI (default: 8000)          |


## API Usage

**POST /chat**

**Request**
```json
{
  "message": "I need to book an appointment for a facial"
}
```

**Response**
```json
{
  "response": "Your appointment has been booked for ..."
}
```

The underlying agent handles intent detection and routes to the appropriate tool.

## Project Architecture

```
clinic-ai-agent/
│
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── config.py          # env var loader
│   ├── agent/             # LangGraph workflow and logic
│   │   ├── graph.py       # defines the workflow graph
│   │   ├── state.py       # TypedDict state schema
│   │   ├── nodes.py       # node implementations
│   │   ├── router.py      # conditional routing logic
│   │   └── prompts.py     # LLM prompts templates
│   ├── tools/             # tools invoked by graph nodes
│   │   ├── booking_tool.py
│   │   ├── reschedule_tool.py
│   │   ├── cancel_tool.py
│   │   ├── faq_tool.py
│   │   └── email_tool.py
│   ├── db/                # database layer
│   │   ├── database.py
│   │   └── models.py
│   └── services/          # external services sim
│       ├── calendar_service.py
│       └── email_service.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

The agent uses LangGraph to determine intent and route to specialized nodes. Each node calls a corresponding tool which interacts with the database or LLM.

---

For more details, review the source code files.
