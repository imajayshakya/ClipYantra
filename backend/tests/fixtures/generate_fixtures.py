#!/usr/bin/env python3
"""Generate synthetic test audio fixtures for ING-003 transcription tests.

This script creates actual WAV files using ffmpeg for integration testing.
Run this once to populate test fixtures with real audio data.
"""

import subprocess
import sys
from pathlib import Path


def generate_fixtures():
    """Generate all test audio fixtures."""
    fixtures_dir = Path(__file__).parent
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ffmpeg not found. Skipping fixture generation.")
        print("Install ffmpeg to generate real audio test fixtures.")
        return
    
    print("Generating test audio fixtures...")
    
    # 1. 10-second sine wave (English-like test)
    print("Generating audio_10s.wav (10s sine wave)...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", 
        "-i", "sine=frequency=440:duration=10",
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(fixtures_dir / "audio_10s.wav")
    ], capture_output=True)
    
    # 2. 45-minute sine wave (long audio test)
    print("Generating audio_45m.wav (45min sine wave)...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "sine=frequency=440:duration=2700",
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(fixtures_dir / "audio_45m.wav")
    ], capture_output=True)
    
    # 3. Corrupted WAV (truncated valid WAV)
    print("Generating audio_corrupt.wav (truncated)...")
    # First generate a valid 10s WAV, then truncate it
    valid_path = fixtures_dir / "audio_10s.wav"
    corrupt_path = fixtures_dir / "audio_corrupt.wav"
    if valid_path.exists():
        # Read valid WAV and truncate to 100 bytes (corrupts it)
        with open(valid_path, "rb") as f:
            data = f.read()
        with open(corrupt_path, "wb") as f:
            f.write(data[:100])  # Only first 100 bytes - corrupts WAV structure
    
    # 4. Spanish-like test (different frequency to simulate different audio)
    print("Generating audio_spanish.wav (10s different tone)...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", "sine=frequency=880:duration=10",  # Higher pitch
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(fixtures_dir / "audio_spanish.wav")
    ], capture_output=True)
    
    print("Done! Fixtures generated in:", fixtures_dir)
    
    # Verify files
    for name in ["audio_10s.wav", "audio_45m.wav", "audio_corrupt.wav", "audio_spanish.wav"]:
        path = fixtures_dir / name
        if path.exists():
            size = path.stat().st_size
            print(f"  {name}: {size} bytes")
        else:
            print(f"  {name}: MISSING")


if __name__ == "__main__":
    generate_fixtures()