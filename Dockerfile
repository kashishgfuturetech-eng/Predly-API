FROM python:3.11-slim

# Install Node.js 18+ and tools
RUN apt-get update \
  && apt-get install -y --no-install-recommends nodejs npm curl \
  && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# ── Python deps ──────────────────────────────────────
COPY backend/pyproject.toml backend/uv.lock ./backend/
RUN cd backend && uv sync --frozen

# ── Frontend: install + build ─────────────────────────
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci --prefix frontend

COPY frontend/ ./frontend/
# VITE_API_BASE_URL is intentionally empty → calls go to /api on same origin
RUN VITE_API_BASE_URL="" npm run build --prefix frontend

# ── Backend source ────────────────────────────────────
COPY backend/ ./backend/
COPY static/ ./static/

EXPOSE 10000

CMD ["bash", "-c", "cd backend && uv run python run.py"]