"""
Transcription Tasks for ClipYantra.

Handles speech-to-text, speaker diarization, transcript alignment,
and translation operations.

Related Requirements: TRC-001, TRC-002, TRC-003
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from celery import shared_task

from app.config import settings
from app.processors.whisper_processor import WhisperProcessor
from app.processors.base import TranscriptionResult, DiarizationResult


@dataclass
class TranscriptionTaskResult:
    """Result of transcription task."""
    success: bool
    job_id: Optional[str] = None
    transcription: Optional[TranscriptionResult] = None
    diarization: Optional[DiarizationResult] = None
    error: Optional[str] = None


@shared_task(
    bind=True,
    name="app.tasks.transcription.transcribe_audio",
    queue="transcription",
    max_retries=3,
    default_retry_delay=120,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def transcribe_audio(
    self,
    file_path: str,
    job_id: str,
    language: Optional[str] = None,
    model: Optional[str] = None,
    task: str = "transcribe",
) -> Dict[str, Any]:
    """
    Transcribe audio from media file using Whisper.
    
    Args:
        file_path: Path to audio/video file
        job_id: Unique transcription job identifier
        language: Language code (None for auto-detect)
        model: Whisper model size (None for default)
        task: "transcribe" or "translate"
        
    Returns:
        Transcription result with segments, words, and metadata
    """
    try:
        processor = WhisperProcessor(
            model_size=model or settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )
        
        # Extract audio if needed
        audio_path = file_path
        if not _is_audio_file(file_path):
            audio_path = _extract_audio(file_path, job_id)
        
        # Transcribe
        result = processor.transcribe(
            audio_path=audio_path,
            language=language or settings.WHISPER_LANGUAGE,
            task=task,
        )
        
        # Clean up extracted audio if temporary
        if audio_path != file_path and audio_path.startswith(tempfile.gettempdir()):
            Path(audio_path).unlink(missing_ok=True)
        
        return {
            "success": True,
            "job_id": job_id,
            "transcription": result.to_dict() if result else None,
            "language": result.language if result else None,
            "duration": result.duration if result else None,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.transcription.diarize_speakers",
    queue="transcription",
    max_retries=2,
    default_retry_delay=60,
)
def diarize_speakers(
    self,
    file_path: str,
    job_id: str,
    max_speakers: Optional[int] = None,
    min_speakers: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Perform speaker diarization on audio file.
    
    Args:
        file_path: Path to audio/video file
        job_id: Unique diarization job identifier
        max_speakers: Maximum number of speakers
        min_speakers: Minimum number of speakers
        
    Returns:
        Diarization result with speaker segments
    """
    try:
        processor = WhisperProcessor(
            model_size=settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )
        
        # Extract audio if needed
        audio_path = file_path
        if not _is_audio_file(file_path):
            audio_path = _extract_audio(file_path, job_id)
        
        # Diarize
        result = processor.diarize(
            audio_path=audio_path,
            max_speakers=max_speakers or settings.TRANSCRIPTION_MAX_SPEAKERS,
            min_speakers=min_speakers,
        )
        
        # Clean up extracted audio if temporary
        if audio_path != file_path and audio_path.startswith(tempfile.gettempdir()):
            Path(audio_path).unlink(missing_ok=True)
        
        return {
            "success": True,
            "job_id": job_id,
            "diarization": result.to_dict() if result else None,
            "num_speakers": result.num_speakers if result else 0,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.transcription.align_transcript",
    queue="transcription",
    max_retries=2,
    default_retry_delay=30,
)
def align_transcript(
    self,
    transcription_json: str,
    diarization_json: str,
    job_id: str,
) -> Dict[str, Any]:
    """
    Align transcription with speaker diarization.
    
    Combines Whisper transcription segments with pyannote speaker labels
    to produce speaker-attributed transcript.
    
    Args:
        transcription_json: JSON string of transcription result
        diarization_json: JSON string of diarization result
        job_id: Unique alignment job identifier
        
    Returns:
        Aligned transcript with speaker labels
    """
    try:
        transcription = TranscriptionResult.from_json(transcription_json)
        diarization = DiarizationResult.from_json(diarization_json)
        
        # Align segments with speakers
        aligned_segments = _align_segments(transcription.segments, diarization.segments)
        
        # Build aligned result
        aligned_result = TranscriptionResult(
            text=transcription.text,
            language=transcription.language,
            duration=transcription.duration,
            segments=aligned_segments,
            words=transcription.words,
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "aligned_transcription": aligned_result.to_dict(),
            "speakers": diarization.speakers if diarization else [],
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.transcription.translate_transcript",
    queue="transcription",
    max_retries=2,
    default_retry_delay=60,
)
def translate_transcript(
    self,
    transcription_json: str,
    job_id: str,
    target_language: str = "en",
) -> Dict[str, Any]:
    """
    Translate transcript to target language.
    
    Args:
        transcription_json: JSON string of transcription result
        job_id: Unique translation job identifier
        target_language: Target language code
        
    Returns:
        Translated transcript
    """
    try:
        transcription = TranscriptionResult.from_json(transcription_json)
        
        # Use Whisper for translation (transcribe with task="translate")
        # Or use a dedicated translation model
        processor = WhisperProcessor(
            model_size=settings.WHISPER_MODEL,
            device=settings.WHISPER_DEVICE,
            compute_type=settings.WHISPER_COMPUTE_TYPE,
        )
        
        # For now, translate each segment
        translated_segments = []
        for segment in transcription.segments:
            translated_text = _translate_text(segment.text, target_language)
            translated_segments.append({
                **segment,
                "text": translated_text,
                "original_text": segment.text,
            })
        
        translated_result = TranscriptionResult(
            text=" ".join(s["text"] for s in translated_segments),
            language=target_language,
            duration=transcription.duration,
            segments=translated_segments,
            words=transcription.words,
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "translated_transcription": translated_result.to_dict(),
            "source_language": transcription.language,
            "target_language": target_language,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


def _is_audio_file(file_path: str) -> bool:
    """Check if file is audio based on extension."""
    audio_extensions = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".opus"}
    return Path(file_path).suffix.lower() in audio_extensions


def _extract_audio(video_path: str, job_id: str) -> str:
    """Extract audio from video file."""
    import subprocess
    
    output_path = Path(tempfile.gettempdir()) / f"{job_id}_audio.wav"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        str(output_path),
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return str(output_path)


def _align_segments(
    transcription_segments: List[Dict],
    diarization_segments: List[Dict],
) -> List[Dict]:
    """Align transcription segments with speaker diarization."""
    aligned = []
    
    for t_seg in transcription_segments:
        t_start = t_seg.get("start", 0)
        t_end = t_seg.get("end", 0)
        t_mid = (t_start + t_end) / 2
        
        # Find overlapping diarization segment
        speaker = "UNKNOWN"
        max_overlap = 0
        
        for d_seg in diarization_segments:
            d_start = d_seg.get("start", 0)
            d_end = d_seg.get("end", 0)
            
            overlap_start = max(t_start, d_start)
            overlap_end = min(t_end, d_end)
            overlap = max(0, overlap_end - overlap_start)
            
            if overlap > max_overlap:
                max_overlap = overlap
                speaker = d_seg.get("speaker", "UNKNOWN")
        
        aligned.append({
            **t_seg,
            "speaker": speaker,
        })
    
    return aligned


def _translate_text(text: str, target_language: str) -> str:
    """Translate text to target language (placeholder)."""
    # In production, use a translation service (Google Translate, DeepL, etc.)
    # For now, return original text
    return text


# TRC-001: Speech-to-text transcription
# TRC-002: Speaker diarization
# TRC-003: Transcript alignment and translation