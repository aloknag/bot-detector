"""
Main FastAPI backend for RBI Bot Detection.
"""

from typing import List, Dict, Any
import logging
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# Configure logging to output to stdout for Docker
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
# Use Uvicorn's logger to ensure logs appear in container logs
logger = logging.getLogger("uvicorn")

app = FastAPI(title="RBI Bot Detection Backend", version="1.0.0")

# Allow CORS for front-end dev and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
sessions: Dict[str, dict] = {}


class SessionData(BaseModel):
    """Data model for a session."""

    session_id: str
    timestamp: float
    environment: str
    score: int
    issues: List[str] = []
    details: Dict[str, Any] = {}
    headers: Dict[str, Any] = {}

    def __init__(self, **data):
        if "issues" not in data:
            data["issues"] = []
        if "details" not in data:
            data["details"] = {}
        if "headers" not in data:
            data["headers"] = {}
        super().__init__(**data)


class SessionSummary(BaseModel):
    """Summary model for a session."""

    id: str
    timestamp: float


@app.get(
    "/api/headers",
    response_class=JSONResponse,
    summary="Get request headers",
)
def get_headers(request: Request, session_id: str = None):
    """
    Get all request headers as a JSON response and optionally save them for a session_id.
    """
    logger.info("***Received request for /api/headers from %s", request.client.host)
    logger.debug("***Request headers: %s", request.headers)
    headers_dict = dict(request.headers)
    # If session_id is provided, save headers for that session
    if session_id:
        if session_id not in sessions:
            sessions[session_id] = {"session_id": session_id}
        sessions[session_id]["headers"] = headers_dict
        logger.info("***Saved headers for session %s", session_id)
    return JSONResponse(content=headers_dict)


@app.get("/api/session", response_model=dict)
def get_new_session():
    """
    Generate a new session_id and create an empty session.
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = {"session_id": session_id}
    logger.info("***Created new session %s", session_id)
    return {"session_id": session_id}


@app.post("/api/sessions", response_model=SessionSummary)
def save_session(session: SessionData):
    """
    Save a session and return its summary.
    """
    session_id = session.session_id or str(uuid.uuid4())
    session_dict = session.model_dump()
    sessions[session_id] = session_dict
    logger.info("***Saved session %s", session_id)
    return SessionSummary(
        id=session_id,
        timestamp=session.timestamp,
        environment=session.environment,
        score=session.score,
    )


@app.post("/api/sessions/partial", response_model=dict)
def save_partial_session(data: dict):
    """
    Save or update partial session data for a session_id.
    """
    session_id = data.get("session_id")
    if not session_id:
        logger.info("***No session_id provided, generating a new one.")
        session_id = str(uuid.uuid4())
    if session_id not in sessions:
        logger.info("***Session %s not found, creating a new one.", session_id)
        sessions[session_id] = {"session_id": session_id}
    # Append to issues
    if "issues" in data:
        sessions[session_id].setdefault("issues", [])
        for issue in data["issues"]:
            if issue not in sessions[session_id]["issues"]:
                sessions[session_id]["issues"].append(issue)
    # Update details (merge dicts)
    if "details" in data:
        sessions[session_id].setdefault("details", {})
        if isinstance(data["details"], dict):
            sessions[session_id]["details"].update(data["details"])
    # Update headers (replace)
    if "headers" in data:
        sessions[session_id]["headers"] = data["headers"]
    # Set environment if present
    if "environment" in data:
        sessions[session_id]["environment"] = data["environment"]
    # Set timestamp if present
    if "timestamp" in data:
        sessions[session_id]["timestamp"] = data["timestamp"]
    logger.info("***Updated session %s with data: %s", session_id[:5], sessions[session_id])
    return {"session_id": session_id}


@app.delete("/api/sessions", response_model=dict)
def clear_sessions():
    """
    Clear all sessions from memory.
    """
    sessions.clear()
    logger.info("***All sessions cleared.")
    return {"status": "cleared"}


@app.get("/api/sessions", response_model=List[SessionSummary])
def list_sessions():
    """
    Return session_id and timestamp for all sessions, latest first.
    """
    summaries = []
    for sid, s in sessions.items():
        ts = s.get("timestamp", 0)
        summaries.append(SessionSummary(id=sid, timestamp=ts))
    logger.info("***Listing all sessions, count: %d", len(summaries))
    return sorted(summaries, key=lambda x: x.timestamp, reverse=True)


@app.get("/api/sessions/{session_id}", response_model=SessionData)
def get_session(session_id: str):
    """
    Get a session by its ID. If not found or missing required fields, return empty/null fields.
    """
    logger.info("***Fetching session data for session_id: %s", session_id)
    s = sessions.get(session_id)
    # Defensive: fill missing required fields with defaults
    if not s:
        return SessionData(
            session_id=session_id,
            timestamp=0,
            environment="",
            score=0,
            issues=[],
            details={},
            headers={},
        )
    logger.debug("***Session data found: %s", s)
    return SessionData(
        session_id=s.get("session_id", session_id),
        timestamp=s.get("timestamp", 0),
        environment=s.get("environment", ""),
        score=s.get("score", 0),
        issues=s.get("issues", []),
        details=s.get("details", {}),
        headers=s.get("headers", {}),
    )


# Uncomment below to run with uvicorn directly
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
