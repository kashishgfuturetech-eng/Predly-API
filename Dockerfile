FROM python:3.11

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# Copy uv package manager
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first (for Docker cache)
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY backend/pyproject.toml backend/uv.lock ./backend/

# Install all dependencies
RUN npm ci \
  && npm ci --prefix frontend \
  && cd backend && uv sync --frozen

# Copy all source code
COPY . .

# Build the Vue frontend (bakes in the API URL at build time)
RUN cd frontend && VITE_API_BASE_URL=https://predly-api.onrender.com/api npm run build

EXPOSE 10000

# Start only the Python backend (it will also serve the built frontend)
CMD cd backend && uv run gunicorn -c gunicorn.conf.py run:application