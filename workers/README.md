# ClipYantra Workers

Background workers for ClipYantra media processing platform. Handles video ingestion, transcription, analysis, and rendering tasks using Celery with Redis broker.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Backend   │────▶│    Redis    │◀───▶│   Workers   │
│   (API)     │     │  (Broker)   │     │  (Celery)   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │  Results    │     │  PostgreSQL │
                    │  Backend    │     │  (Metadata) │
                    └─────────────┘     └─────────────┘
```

## Task Queues

| Queue | Tasks | Concurrency | Priority |
|-------|-------|-------------|----------|
| `ingestion` | Media validation, metadata extraction, thumbnails, proxies | 4 | High |
| `transcription` | Whisper ASR, speaker diarization, alignment | 2 | High |
| `analysis` | Scene detection, face detection, content analysis | 2 | Normal |
| `rendering` | Video composition, caption rendering, exports | 1 | Low |
| `default` | Fallback queue | 2 | Normal |

## Quick Start

### Prerequisites

- Python 3.11+
- Redis 7+
- PostgreSQL 15+
- FFmpeg 6+
- (Optional) NVIDIA GPU with CUDA for faster transcription

### Installation

```bash
# Clone and navigate
cd workers

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Or use uv (faster)
uv sync --all-extras
```

### Configuration

```bash
# Copy example environment
cp .env.example .env

# Edit configuration
vim .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `DIARIZATION_AUTH_TOKEN` - Hugging Face token for speaker diarization (optional)

### Running Workers

```bash
# Development (with hot reload)
celery -A app.celery_app worker --loglevel=info --concurrency=4

# Specific queues only
celery -A app.celery_app worker --loglevel=info -Q ingestion,transcription

# With beat scheduler (periodic tasks)
celery -A app.celery_app beat --loglevel=info

# Combined worker + beat (dev only)
celery -A app.celery_app worker --beat --loglevel=info

# Production
celery -A app.celery_app worker \
  --loglevel=info \
  --concurrency=4 \
  --max-tasks-per-child=1000 \
  --prefetch-multiplier=1 \
  --queues=ingestion,transcription,analysis,rendering,default \
  --hostname=worker@%h
```

### Docker

```bash
# Development
docker build --target development -t clipyantra-workers:dev .
docker run --rm -it \
  --env-file .env \
  -v $(pwd):/app \
  clipyantra-workers:dev

# Production
docker build --target production -t clipyantra-workers:prod .
docker run --rm -d \
  --env-file .env \
  -v clipyantra-data:/app/data \
  clipyantra-workers:prod
```

### Docker Compose (Recommended)

From project root:
```bash
# Start all services
docker-compose -f infra/docker/docker-compose.yml up -d

# With dev overrides
docker-compose -f infra/docker/docker-compose.yml -f infra/docker/docker-compose.dev.yml up -d

# View logs
docker-compose logs -f worker
```

## Task Modules

### Ingestion Tasks (`app/tasks/ingestion.py`)

| Task | Description | Queue |
|------|-------------|-------|
| `validate_media` | Validate file format, duration, codecs | ingestion |
| `extract_metadata` | Extract duration, dimensions, bitrate, streams | ingestion |
| `generate_thumbnails` | Generate thumbnails at intervals | ingestion |
| `generate_proxy` | Create low-res proxy for editing | ingestion |
| `generate_sprite` | Create thumbnail sprite sheet | ingestion |
| `cleanup_expired_uploads` | Remove stale upload files (periodic) | ingestion |

### Transcription Tasks (`app/tasks/transcription.py`)

| Task | Description | Queue |
|------|-------------|-------|
| `transcribe_media` | Run Whisper ASR on audio | transcription |
| `diarize_audio` | Speaker diarization with pyannote | transcription |
| `align_transcription` | Align transcript with audio (word-level) | transcription |
| `translate_transcription` | Translate transcript to target language | transcription |

### Analysis Tasks (`app/tasks/analysis.py`)

| Task | Description | Queue |
|------|-------------|-------|
| `detect_scenes` | Detect scene boundaries | analysis |
| `detect_faces` | Detect and track faces | analysis |
| `analyze_content` | Content classification, NSFW detection | analysis |
| `generate_daily_analytics` | Aggregate daily metrics (periodic) | analysis |

### Rendering Tasks (`app/tasks/rendering.py`)

| Task | Description | Queue |
|------|-------------|-------|
| `compose_video` | Compose timeline into video | rendering |
| `render_captions` | Burn captions into video | rendering |
| `export_video` | Export with preset | rendering |
| `create_clip` | Extract sub-clip | rendering |

## Processors

### FFmpeg Processor (`app/processors/ffmpeg_processor.py`)

Wrapper around FFmpeg with typed interfaces:

```python
from app.processors import FFmpegProcessor, MediaMetadata

processor = FFmpegProcessor()

# Validate media
result = await processor.validate_media("input.mp4")

# Extract metadata
metadata: MediaMetadata = await processor.extract_metadata("input.mp4")

# Generate thumbnails
thumbnails = await processor.generate_thumbnails(
    "input.mp4", 
    output_dir="/thumbnails",
    interval=10.0,
    count=10
)

# Transcode to proxy
proxy_path = await processor.transcode_proxy(
    "input.mp4",
    output_dir="/proxies",
    resolution="854x480"
)

# Detect scenes
scenes = await processor.detect_scenes("input.mp4", threshold=30.0)

# Analyze audio
audio_data = await processor.analyze_audio("input.mp4")
```

### Whisper Processor (`app/processors/whisper_processor.py`)

High-level transcription with faster-whisper:

```python
from app.processors import WhisperProcessor, TranscriptionResult

processor = WhisperProcessor(
    model_size="base",
    device="cpu",
    compute_type="int8"
)

# Transcribe
result: TranscriptionResult = await processor.transcribe(
    "audio.wav",
    language="en",
    task="transcribe"
)

# With diarization
result = await processor.transcribe_with_diarization(
    "audio.wav",
    diarization_model="pyannote/speaker-diarization-3.1",
    auth_token="hf_token"
)

# Align (word-level timestamps)
aligned = await processor.align_transcription("audio.wav", result)
```

## Data Models

All processors return typed dataclasses:

- `MediaMetadata` - Video/audio metadata
- `TranscriptionResult` - Transcript with segments
- `DiarizationResult` - Speaker segments
- `SceneDetectionResult` - Scene boundaries
- `FaceDetectionResult` - Face tracks
- `ContentAnalysisResult` - Classification results
- `RenderResult` - Render output info
- `RenderPreset` - Export presets

## Monitoring

### Prometheus Metrics

Available at `:9090/metrics` when enabled:

- `celery_tasks_total` - Tasks processed by type/status
- `celery_task_duration_seconds` - Task latency histogram
- `celery_workers_active` - Active worker count
- `celery_queue_length` - Queue depth
- `media_processing_duration_seconds` - Processing time by operation
- `transcription_duration_seconds` - Transcription time
- `render_duration_seconds` - Render time

### Health Checks

```bash
# Celery ping
celery -A app.celery_app inspect ping

# Active tasks
celery -A app.celery_app inspect active

# Registered tasks
celery -A app.celery_app inspect registered

# Worker stats
celery -A app.celery_app inspect stats
```

### Logging

Structured JSON logging via structlog. Configure via `LOG_LEVEL` and `LOG_FORMAT=json`.

## Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/unit/test_ffmpeg_processor.py -v
```

### Test Fixtures

- `tests/conftest.py` - Shared fixtures
- `tests/fixtures/` - Test media files

## Development

### Code Style

```bash
# Format
ruff format .
black .

# Lint
ruff check . --fix
mypy app/

# Sort imports
isort .
```

### Pre-commit

```bash
pre-commit install
pre-commit run --all-files
```

### Adding New Tasks

1. Create task in appropriate `app/tasks/*.py`
2. Register in `app/tasks/__init__.py`
3. Add route in `app/celery_app.py` if new queue needed
4. Write tests in `tests/unit/tasks/`
5. Update this README

## Deployment

### Kubernetes

```yaml
# See infra/k8s/base/deployment.yaml for worker deployment
# Override replicas in overlays/prod/kustomization.yaml
```

### Scaling

- **Horizontal**: Increase worker replicas per queue
- **Vertical**: Adjust `--concurrency` per worker
- **Queue-specific**: Deploy dedicated workers per queue

```bash
# Dedicated transcription workers (GPU)
celery -A app.celery_app worker -Q transcription --concurrency=1 --pool=gevent

# High-throughput ingestion
celery -A app.celery_app worker -Q ingestion --concurrency=8
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `uv sync` or `pip install -e .` |
| `Redis connection refused` | Check `REDIS_URL` and Redis server |
| `CUDA out of memory` | Reduce batch size, use smaller model |
| `FFmpeg not found` | Install FFmpeg: `apt-get install ffmpeg` |
| `Diarization fails` | Set `DIARIZATION_AUTH_TOKEN` from Hugging Face |

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG celery -A app.celery_app worker --loglevel=debug

# Inspect task
celery -A app.celery_app inspect query_task <task_id>
```

## License

MIT License - see LICENSE file for details.