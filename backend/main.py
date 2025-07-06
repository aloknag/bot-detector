from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="RBI Bot Detection Backend", version="1.0.0")

# Allow CORS for front-end dev and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data model for a session
class SessionData(BaseModel):
    """
    Session data
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique session identifier"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="ISO timestamp of session",
    )
    environment: str = Field(..., example="RBI")
    score: int = Field(..., ge=0, le=100, example=85)
    issues: List[str] = Field(default_factory=list)


# In-memory store for sessions
sessions: List[SessionData] = []


@app.get(
    "/api/sessions",
    response_model=List[SessionData],
    summary="Get all bot detection sessions",
)
def get_sessions():
    """Retrieve all stored bot detection sessions."""
    return sessions


@app.post("/api/sessions", status_code=201, summary="Add a full session record")
def add_session(data: SessionData):
    """Add a full session payload including ID and timestamp."""
    sessions.append(data)
    return {"message": "Session added", "id": data.id}


@app.post(
    "/api/sessions/create",
    status_code=201,
    summary="Create a session from minimal input",
)
def create_session(payload: dict):
    """
    Create a new session using only partial data. ID and timestamp are generated automatically.
    """
    try:
        session = SessionData(
            environment=payload.get("environment", "Unknown"),
            score=payload.get("score", 0),
            issues=payload.get("issues", []),
        )
        sessions.append(session)
        return {"message": "Session created", "id": session.id}
    except Exception as e:  # pylint-disable=broad-except
        raise HTTPException(status_code=400, detail=f"Invalid payload: {e}") from e


# Uncomment below to run with uvicorn directly
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
