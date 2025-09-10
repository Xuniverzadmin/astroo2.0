# Multi-stage build for production and development
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies including tzdata for timezone support
RUN apt-get update && apt-get install -y \
    tzdata \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set timezone
ENV TZ=UTC

WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-cov \
    httpx \
    black \
    flake8 \
    mypy

# Copy application code
COPY backend/ /app

# Expose port
EXPOSE 8000

# Development command with auto-reload
CMD ["uvicorn", "numerology_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production

# Copy application code
COPY backend/ /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

# Production command
CMD ["uvicorn", "numerology_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]