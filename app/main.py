from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.config import settings
from app.agent.graph import create_agent_graph
from app.db import database, models

# create database tables on startup
from app.db.database import Base
Base.metadata.create_all(bind=database.engine)

app = FastAPI()
agent_graph = create_agent_graph()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    state = {"raw_message": req.message}
    try:
        final_state = agent_graph.run(state)
        res = final_state.get("response", "")
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
