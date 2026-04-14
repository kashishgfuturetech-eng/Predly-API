# ============ Stage 1: Build frontend ============
FROM node:20-slim AS frontend-builder

WORKDIR /app

COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/

RUN npm ci --omit=dev \
  && npm ci --prefix frontend

COPY frontend/ ./frontend/

RUN cd frontend && VITE_API_BASE_URL=https://your-app.up.railway.app/api npm run build

# ============ Stage 2: Build Python deps ============
FROM python:3.11-slim AS python-builder

RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc g++ curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

ENV UV_PYTHON=/usr/local/bin/python3
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app/backend

COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

# ============ Stage 3: Final image ============
FROM python:3.11-slim AS final

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

ENV UV_PYTHON=/usr/local/bin/python3
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Copy only the virtual environment from builder
COPY --from=python-builder /app/backend/.venv ./backend/.venv

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy backend source only
COPY backend/ ./backend/

EXPOSE 10000

CMD ["sh", "-c", "cd /app/backend && uv run gunicorn --timeout 600 --graceful-timeout 300 -c gunicorn.conf.py run:application"]