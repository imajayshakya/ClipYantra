# ClipYantra Docker Infrastructure

## Overview

This directory contains Docker Compose configurations for local development, development override, and production deployment.

## Files

- `docker-compose.yml` - Base configuration for local development
- `docker-compose.dev.yml` - Development override with hot reload and debug ports
- `docker-compose.prod.yml` - Production configuration with replicas, resource limits, and SSL
- `nginx/` - Nginx reverse proxy configurations
  - `nginx.conf` - Base nginx config
  - `nginx.dev.conf` - Development nginx config
  - `nginx.prod.conf` - Production nginx config with SSL
  - `conf.d/` - Additional nginx configuration snippets

## Quick Start

### Development
```bash
# Start all services with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.yml -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

### Production
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with production values

# Deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale worker=4
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| nginx | 80/443 | Reverse proxy, SSL termination |
| frontend | 3000 | Next.js frontend |
| backend | 8000 | FastAPI backend |
| worker | - | Celery workers (background jobs) |
| postgres | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache & Celery broker |

## Environment Variables

Create a `.env` file in this directory with:

```env
# Database
POSTGRES_DB=clipyantra
POSTGRES_USER=clipyantra
POSTGRES_PASSWORD=secure-password

# Redis
REDIS_PASSWORD=secure-redis-password

# Application
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DOMAIN=yourdomain.com

# Worker
WHISPER_MODEL=base
```

## Networks & Volumes

- **Network**: `clipyantra-network` (bridge)
- **Volumes**:
  - `postgres_data` - PostgreSQL data
  - `redis_data` - Redis data
  - `media_storage` - Shared media storage for worker/backend/nginx

## Health Checks

All services include health checks. Use `docker-compose ps` to verify service health.

## Debugging

Backend debug port (dev only): `5678`
Attach VS Code/PyCharm debugger to `localhost:5678`

## SSL Certificates (Production)

Place SSL certificates in `nginx/ssl/`:
- `fullchain.pem` - Full certificate chain
- `privkey.pem` - Private key
- `chain.pem` - Certificate chain (for OCSP stapling)

Use Let's Encrypt or your preferred CA.