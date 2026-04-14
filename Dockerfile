FROM python:3.11-slim

# Install Node.js 20 and minimal system deps
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     curl \
     ca-certificates \
  && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y --no-install-recommends nodejs \
  && rm -rf /var/lib/apt/lists/*

# Copy uv
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

ENV UV_PYTHON=/usr/local/bin/python3
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY backend/pyproject.toml backend/uv.lock ./backend/

RUN npm ci --omit=dev \
  && npm ci --prefix frontend \
  && cd backend && uv sync --frozen --no-cache

# Copy source
COPY . .

# Build frontend
RUN cd frontend && VITE_API_BASE_URL=https://your-app.up.railway.app/api npm run build \
  && rm -rf node_modules frontend/node_modules

EXPOSE 10000

CMD ["sh", "-c", "cd /app/backend && uv run gunicorn --timeout 600 --graceful-timeout 300 -c gunicorn.conf.py run:application"]