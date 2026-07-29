# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# ==========================================
# STAGE 2: Final Production Runtime
# ==========================================
FROM python:3.11-slim as runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

# Expose FastAPI HTTP Port
EXPOSE 8000

# Docker Healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Start Uvicorn ASGI Server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
