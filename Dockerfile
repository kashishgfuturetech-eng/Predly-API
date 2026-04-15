FROM python:3.11-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends nodejs npm curl \
  && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Python deps
COPY backend/pyproject.toml backend/uv.lock ./backend/
RUN cd backend && uv sync --frozen

# Frontend: install + build (run from INSIDE frontend dir, not --prefix)
COPY frontend/ ./frontend/
RUN cd frontend && npm ci && VITE_API_BASE_URL="" npm run build

# Verify dist was created
RUN ls -la /app/frontend/dist && echo "✅ frontend/dist OK"

# Backend source
COPY backend/ ./backend/
COPY static/ ./static/

EXPOSE 10000

CMD ["bash", "-c", "cd backend && uv run python run.py"]