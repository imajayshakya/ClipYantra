# Test Fixtures

This directory contains synthetic test fixtures for ING-002 tests.

Note: Real media files are not committed. Tests use mocked FFprobe responses
and synthetic binary data to validate the ingestion pipeline.

For manual testing with real media:
1. Install FFmpeg: `winget install Gyan.FFmpeg` or download from ffmpeg.org
2. Generate test files: `ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 -c:v libx264 test_video.mp4`
3. Place in this directory (gitignored)