# Dockerfile for FastAPI + Live Sync Worker
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Install dependencies needed for SQLite and building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Setup Supervisor to run both the FastAPI server and the live_sync worker
# This allows running both in one "free tier" container
RUN mkdir -p /etc/supervisor/conf.d
RUN echo "[supervisord]\nnodaemon=true\n\n[program:api]\ncommand=uvicorn backend.main:app --host 0.0.0.0 --port 8000\nautostart=true\nautorestart=true\nstderr_logfile=/var/log/api.err.log\nstdout_logfile=/var/log/api.out.log\n\n[program:worker]\ncommand=python live_sync.py\nautostart=true\nautorestart=true\nstderr_logfile=/var/log/worker.err.log\nstdout_logfile=/var/log/worker.out.log\n" > /etc/supervisor/conf.d/supervisord.conf

# Expose port
EXPOSE 8000

# Start Supervisor (which starts API + Worker)
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
