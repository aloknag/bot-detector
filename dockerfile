# Multi-stage build for serving both backend (FastAPI) and frontend (Vite) with Nginx

# --- Frontend Build Stage ---
FROM node:20 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- Backend Build Stage ---
FROM python:3.11-slim AS backend-build
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# --- Final Stage: Nginx + Backend ---
FROM nginx:alpine

# Copy built frontend to nginx html dir
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy backend code
COPY --from=backend-build /app/backend /app/backend

# Install Python, pip, and create a virtual environment for backend
RUN apk add --no-cache python3 py3-pip && \
    python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir uvicorn fastapi

# Start both backend and nginx using supervisord
RUN apk add --no-cache supervisor
COPY supervisord.conf /etc/supervisord.conf

EXPOSE 80 8000
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
