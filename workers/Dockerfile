# ClipYantra Workers Dockerfile
# Multi-stage build for optimized production image

# =========================================================================
# Base Stage - Common dependencies
# =========================================================================
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # FFmpeg for video/audio processing
    ffmpeg \
    # Build tools for Python packages
    build-essential \
    # For audio processing
    libsndfile1 \
    # For image processing
    libjpeg-dev \
    libpng-dev \
    # For PostgreSQL client
    libpq-dev \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Set work directory
WORKDIR /app

# =========================================================================
# Builder Stage - Install Python dependencies
# =========================================================================
FROM base AS builder

# Install uv for fast package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen --no-dev

# =========================================================================
# Development Stage - With dev dependencies
# =========================================================================
FROM builder AS development

# Install dev dependencies
RUN uv sync --frozen --all-extras

# Copy source code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose ports
EXPOSE 8000 9090

# Default command for development
CMD ["uv", "run", "celery", "-A", "app.celery_app", "worker", "--loglevel=info", "--concurrency=4"]

# =========================================================================
# Production Stage - Minimal runtime
# =========================================================================
FROM base AS production

# Copy only necessary files from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser pyproject.toml ./

# Create data directories
RUN mkdir -p /app/data/{uploads,thumbnails,proxies,renders,exports,clips,analysis} \
    && chown -R appuser:appuser /app/data

# Switch to non-root user
USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD celery -A app.celery_app inspect ping || exit 1

# Expose ports
EXPOSE 8000 9090

# Default command for production
CMD ["celery", "-A", "app.celery_app", "worker", \
     "--loglevel=info", \
     "--concurrency=4", \
     "--max-tasks-per-child=1000", \
     "--prefetch-multiplier=1", \
     "--queues=ingestion,transcription,analysis,rendering,default", \
     "--hostname=worker@%h"]
