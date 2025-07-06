# Bot Detector

A full-stack application for detecting bots and automated browsers using advanced fingerprinting and behavioral analysis. Built with **Vue 3 + Vite** (frontend), **FastAPI** (backend), and served via **Nginx** in a Docker container.

---

## Features

- **Frontend**
    - Modern Vue 3 SPA with Vite and Bootstrap 5
    - Multiple bot detection tests:
        - User activity (keystrokes, mouse, touch)
        - Headless browser detection
        - Fingerprint consistency (OS, timezone, language, hardware)
        - Rendering fingerprint (Canvas/WebGL)
        - Audio and performance entropy
        - Environment anomalies
        - Request headers display
        - [CreepJS](https://abrahamjuliot.github.io/creepjs/) integration
    - Session history with scores and detected issues

- **Backend**
    - FastAPI REST API for session and header data
    - In-memory session storage (no database required)
    - CORS enabled for frontend/backend integration

- **Deployment**
    - Docker multi-stage build: frontend, backend, Nginx
    - Supervisor manages both backend and Nginx in one container
    - GitHub Actions workflow for Docker image build & publish

---

## Quick Start

### 1. Development
> **Note:** For local development, update the backend API URL in your frontend configuration to `http://localhost:8000/`.

#### Frontend

```sh
cd frontend
npm install
npm run dev
```

#### Backend

```sh
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Access

- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8000](http://localhost:8000)

### 2. Production (Docker)

Build and run the full stack with Docker:

```sh
docker build -t bot-detector .
docker run -p 80:80 -p 8000:8000 bot-detector
```

- App available at [http://localhost](http://localhost)

---

## Project Structure

```
bot-detector/
├── backend/         # FastAPI backend
├── frontend/        # Vue 3 + Vite frontend
├── nginx.conf       # Nginx config for SPA + API proxy
├── supervisord.conf # Supervisor config for multi-process
├── dockerfile       # Multi-stage Docker build
```

---

## API Endpoints

- `GET /api/sessions` — List all detection sessions
- `POST /api/sessions` — Add a session (full payload)
- `POST /api/sessions/create` — Add a session (minimal payload)
- `GET /api/headers` — Get incoming request headers

---

## Development Notes

- **Backend**: Sessions are stored in memory; for production, consider adding persistent storage.
- **Docker**: Both backend and frontend are served from a single container using Nginx and Supervisor.

---

## License

MIT (see individual dependencies for their licenses)