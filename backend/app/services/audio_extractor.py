"""ING-003 Audio extraction and chunking using FFmpeg."""

import asyncio
import math
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class AudioChunk:
    """Represents an audio chunk with its absolute timing."""
    path: Path
    start_ms: int
    end_ms: int
    chunk_index: int
    is_overlap: bool = False


@dataclass(frozen=True)
class ExtractionResult:
    """Result of audio extraction."""
    audio_path: Path
    duration_ms: int
    chunks: List[AudioChunk]
    sample_rate: int
    channels: int


class AudioExtractor:
    """Extracts and chunks audio from media files using FFmpeg."""

    # Chunking configuration
    CHUNK_DURATION_MS = 30 * 60 * 1000  # 30 minutes
    OVERLAP_MS = 30 * 1000  # 30 seconds

    def __init__(
        self,
        ffmpeg_path: str = "ffmpeg",
        ffprobe_path: str = "ffprobe",
        chunk_duration_ms: int = CHUNK_DURATION_MS,
        overlap_ms: int = OVERLAP_MS,
    ):
        self.ffmpeg_path = ffmpeg_path
        self.ffprobe_path = ffprobe_path
        self.chunk_duration_ms = chunk_duration_ms
        self.overlap_ms = overlap_ms

    async def extract_audio(
        self,
        input_path: Path,
        output_dir: Optional[Path] = None,
    ) -> ExtractionResult:
        """
        Extract audio from video file to 16kHz mono WAV.
        
        Args:
            input_path: Path to input media file
            output_dir: Directory for output (temp dir if None)
            
        Returns:
            ExtractionResult with audio path, duration, and chunks
        """
        if output_dir is None:
            output_dir = Path(tempfile.mkdtemp(prefix="clipyantra_audio_"))
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get media duration first
        duration_ms = await self._get_duration(input_path)
        
        # Extract full audio to WAV
        audio_filename = f"{input_path.stem}_audio.wav"
        audio_path = output_dir / audio_filename
        
        await self._run_ffmpeg([
            self.ffmpeg_path,
            "-i", str(input_path),
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # 16-bit PCM
            "-ar", "16000",  # 16kHz sample rate
            "-ac", "1",  # Mono
            "-y",  # Overwrite
            str(audio_path),
        ])
        
        # Create chunks if needed
        chunks = await self._create_chunks(audio_path, duration_ms, output_dir)
        
        return ExtractionResult(
            audio_path=audio_path,
            duration_ms=duration_ms,
            chunks=chunks,
            sample_rate=16000,
            channels=1,
        )

    async def _get_duration(self, input_path: Path) -> int:
        """Get media duration in milliseconds using ffprobe."""
        proc = await asyncio.create_subprocess_exec(
            self.ffprobe_path,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(input_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {stderr.decode()}")
        
        duration_sec = float(stdout.decode().strip())
        return int(duration_sec * 1000)

    async def _create_chunks(
        self,
        audio_path: Path,
        duration_ms: int,
        output_dir: Path,
    ) -> List[AudioChunk]:
        """Create audio chunks with overlap for long media."""
        chunks = []
        
        if duration_ms <= self.chunk_duration_ms:
            # Short enough - single chunk
            chunks.append(AudioChunk(
                path=audio_path,
                start_ms=0,
                end_ms=duration_ms,
                chunk_index=0,
                is_overlap=False,
            ))
            return chunks
        
        # Calculate chunk boundaries with overlap
        chunk_starts = []
        pos = 0
        while pos < duration_ms:
            chunk_starts.append(pos)
            pos += self.chunk_duration_ms - self.overlap_ms
        
        # Create chunks using FFmpeg segment
        for i, start_ms in enumerate(chunk_starts):
            end_ms = min(start_ms + self.chunk_duration_ms, duration_ms)
            is_overlap = i > 0  # All except first are overlap chunks
            
            chunk_filename = f"{audio_path.stem}_chunk_{i:03d}.wav"
            chunk_path = output_dir / chunk_filename
            
            # Extract chunk using FFmpeg
            await self._run_ffmpeg([
                self.ffmpeg_path,
                "-i", str(audio_path),
                "-ss", f"{start_ms / 1000:.3f}",
                "-t", f"{(end_ms - start_ms) / 1000:.3f}",
                "-acodec", "copy",
                "-y",
                str(chunk_path),
            ])
            
            chunks.append(AudioChunk(
                path=chunk_path,
                start_ms=start_ms,
                end_ms=end_ms,
                chunk_index=i,
                is_overlap=is_overlap,
            ))
        
        return chunks

    async def _run_ffmpeg(self, cmd: List[str]) -> None:
        """Run FFmpeg command and raise on failure."""
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            raise RuntimeError(
                f"FFmpeg failed (exit {proc.returncode}): {stderr.decode()}"
            )

    @staticmethod
    def merge_segments(
        chunk_results: List["ChunkTranscriptionResult"],
    ) -> List["MergedSegment"]:
        """
        Merge transcription results from overlapping chunks.
        
        Deduplicates overlapping text by comparing timestamps.
        """
        if not chunk_results:
            return []
        
        if len(chunk_results) == 1:
            return [MergedSegment(
                start_ms=s.start_ms,
                end_ms=s.end_ms,
                text=s.text,
                speaker=s.speaker,
                confidence=s.confidence,
                word_alignments=s.word_alignments,
            ) for s in chunk_results[0].segments]
        
        # Sort all segments by start time
        all_segments = []
        for chunk in chunk_results:
            for seg in chunk.segments:
                all_segments.append((chunk.chunk_start_ms + seg.start_ms, seg))
        
        all_segments.sort(key=lambda x: x[0])
        
        # Merge with overlap deduplication
        merged = []
        for abs_start, seg in all_segments:
            abs_end = abs_start + (seg.end_ms - seg.start_ms)
            
            # Check for overlap with previous segment
            if merged and abs_start < merged[-1].end_ms:
                # Overlap detected - keep the one with higher confidence
                prev = merged[-1]
                if seg.confidence and prev.confidence and seg.confidence > prev.confidence:
                    # Replace with higher confidence segment
                    merged[-1] = MergedSegment(
                        start_ms=abs_start,
                        end_ms=abs_end,
                        text=seg.text,
                        speaker=seg.speaker,
                        confidence=seg.confidence,
                        word_alignments=seg.word_alignments,
                    )
                # Otherwise keep previous (first) segment
            else:
                merged.append(MergedSegment(
                    start_ms=abs_start,
                    end_ms=abs_end,
                    text=seg.text,
                    speaker=seg.speaker,
                    confidence=seg.confidence,
                    word_alignments=seg.word_alignments,
                ))
        
        return merged


@dataclass(frozen=True)
class ChunkTranscriptionResult:
    """Result from transcribing a single chunk."""
    chunk_start_ms: int
    chunk_end_ms: int
    segments: List["SegmentResult"]


@dataclass(frozen=True)
class SegmentResult:
    """Single transcription segment from a provider."""
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    word_alignments: Optional[List[dict]] = None


@dataclass(frozen=True)
class MergedSegment:
    """Merged segment with absolute timestamps."""
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    word_alignments: Optional[List[dict]] = None