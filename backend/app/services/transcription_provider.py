"""ING-003 Transcription provider abstractions and implementations."""

import asyncio
import json
import os
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set, Dict, Any

import httpx


@dataclass(frozen=True)
class TranscriptionRequest:
    """Request for transcription."""
    audio_path: Path
    language: Optional[str] = None  # None = auto-detect
    diarization: bool = False
    word_alignments: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            object.__setattr__(self, 'metadata', {})


@dataclass(frozen=True)
class WordAlignment:
    """Word-level alignment."""
    word: str
    start_ms: int
    end_ms: int
    confidence: float


@dataclass(frozen=True)
class SegmentResult:
    """Single transcription segment."""
    start_ms: int
    end_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    word_alignments: Optional[List[WordAlignment]] = None
    words: Optional[List[WordAlignment]] = None  # alias for word_alignments
    
    def __post_init__(self):
        # Maintain backward compatibility - words and word_alignments are the same
        if self.words is not None and self.word_alignments is None:
            object.__setattr__(self, 'word_alignments', self.words)
        elif self.word_alignments is not None and self.words is None:
            object.__setattr__(self, 'words', self.word_alignments)
        elif self.words is None and self.word_alignments is None:
            object.__setattr__(self, 'words', [])
            object.__setattr__(self, 'word_alignments', [])


@dataclass(frozen=True)
class TranscriptionResult:
    """Complete transcription result."""
    full_text: str
    language: str
    segments: List[SegmentResult]
    provider_metadata: Dict[str, Any]


class TranscriptionProvider(ABC):
    """Abstract base class for transcription providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique provider identifier."""
        ...

    @property
    @abstractmethod
    def model_id(self) -> str:
        """Model identifier."""
        ...

    @property
    def supports_diarization(self) -> bool:
        """Whether provider supports speaker diarization."""
        return False

    @property
    def supports_word_alignments(self) -> bool:
        """Whether provider supports word-level alignments."""
        return False

    @property
    def supported_languages(self) -> Set[str]:
        """Supported language codes (ISO 639-1)."""
        return {"en"}

    @abstractmethod
    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        """Transcribe audio and return result."""
        ...

    def validate_request(self, request: TranscriptionRequest) -> None:
        """Validate request against provider capabilities."""
        if request.diarization and not self.supports_diarization:
            raise ValueError(f"{self.provider_name} does not support diarization")
        if request.word_alignments and not self.supports_word_alignments:
            raise ValueError(f"{self.provider_name} does not support word alignments")
        if request.language and request.language not in self.supported_languages:
            raise ValueError(
                f"{self.provider_name} does not support language: {request.language}"
            )

    @classmethod
    def validate_capabilities(cls, provider: 'TranscriptionProvider', language: str = None, diarization: bool = False, word_alignments: bool = False) -> None:
        """Validate capabilities against a provider instance."""
        if diarization and not provider.supports_diarization:
            raise ValueError(f"{provider.provider_name} does not support diarization")
        if word_alignments and not provider.supports_word_alignments:
            raise ValueError(f"{provider.provider_name} does not support word_alignments")
        if language and language not in provider.supported_languages:
            raise ValueError(
                f"{provider.provider_name} does not support language: {language}"
            )


class WhisperXProvider(TranscriptionProvider):
    """Local WhisperX transcription provider."""

    def __init__(
        self,
        model: str = "large-v3",
        device: str = "auto",
        compute_type: str = "float16",
        hf_token: Optional[str] = None,
    ):
        self._model_name = model
        self._device = device
        self._compute_type = compute_type
        self._hf_token = hf_token
        self._model = None

    @property
    def provider_name(self) -> str:
        return "whisperx"

    @property
    def model_id(self) -> str:
        return f"whisper-{self._model_name}"

    @property
    def supports_diarization(self) -> bool:
        return True

    @property
    def supports_word_alignments(self) -> bool:
        return True

    @property
    def supported_languages(self) -> Set[str]:
        return {"en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "ja", "ko", "zh"}

    def _load_model(self):
        """Lazy load WhisperX model."""
        if self._model is None:
            try:
                import whisperx
                import torch
                
                if self._device == "auto":
                    device = "cuda" if torch.cuda.is_available() else "cpu"
                else:
                    device = self._device
                
                self._model = whisperx.load_model(
                    self._model_name,
                    device,
                    compute_type=self._compute_type,
                )
            except ImportError:
                raise RuntimeError(
                    "WhisperX not installed. Install with: pip install whisperx"
                )

    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        self.validate_request(request)
        self._load_model()
        
        import whisperx
        
        # Load audio
        audio = whisperx.load_audio(str(request.audio_path))
        
        # Transcribe
        result = self._model.transcribe(
            audio,
            language=request.language,
            batch_size=16,
        )
        
        # Align if requested
        word_alignments = None
        if request.word_alignments:
            try:
                model_a, metadata = whisperx.load_align_model(
                    language_code=result["language"],
                    device=self._device if self._device != "auto" else "cuda",
                )
                result = whisperx.align(
                    result["segments"],
                    model_a,
                    metadata,
                    audio,
                    self._device if self._device != "auto" else "cuda",
                )
                word_alignments = True
            except Exception:
                word_alignments = False
        
        # Diarization if requested
        speaker_segments = None
        if request.diarization:
            try:
                diarize_model = whisperx.DiarizationPipeline(
                    use_auth_token=self._hf_token,
                    device=self._device if self._device != "auto" else "cuda",
                )
                diarize_segments = diarize_model(audio)
                result = whisperx.assign_word_speakers(diarize_segments, result)
                speaker_segments = diarize_segments
            except Exception:
                pass
        
        # Build segments
        segments = []
        full_text_parts = []
        
        for seg in result.get("segments", []):
            start_ms = int(seg["start"] * 1000)
            end_ms = int(seg["end"] * 1000)
            text = seg["text"].strip()
            
            speaker = seg.get("speaker")
            if speaker_segments is not None and "speaker" not in seg:
                # Find speaker from diarization
                for dseg in speaker_segments:
                    if dseg["start"] <= seg["start"] < dseg["end"]:
                        speaker = dseg["speaker"]
                        break
            
            # Word alignments
            alignments = None
            if word_alignments and "words" in seg:
                alignments = [
                    WordAlignment(
                        word=w["word"],
                        start_ms=int(w["start"] * 1000),
                        end_ms=int(w["end"] * 1000),
                        confidence=w.get("score", 0.0),
                    )
                    for w in seg["words"]
                ]
            
            segments.append(SegmentResult(
                start_ms=start_ms,
                end_ms=end_ms,
                text=text,
                speaker=speaker,
                confidence=seg.get("avg_logprob"),
                word_alignments=alignments,
            ))
            full_text_parts.append(text)
        
        full_text = " ".join(full_text_parts)
        
        return TranscriptionResult(
            full_text=full_text,
            language=result.get("language", request.language or "en"),
            segments=segments,
            provider_metadata={
                "model": self.model_id,
                "device": self._device,
                "compute_type": self._compute_type,
            },
        )


class DeepgramProvider(TranscriptionProvider):
    """Deepgram cloud transcription provider."""

    def __init__(self, api_key: str, model: str = "nova-2"):
        if not api_key:
            raise ValueError("Deepgram API key required")
        self._api_key = api_key
        self._model = model
        self._base_url = "https://api.deepgram.com/v1/listen"

    @property
    def provider_name(self) -> str:
        return "deepgram"

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_diarization(self) -> bool:
        return True

    @property
    def supports_word_alignments(self) -> bool:
        return True

    @property
    def supported_languages(self) -> Set[str]:
        return {"en", "es", "fr", "de", "it", "pt", "nl", "hi", "ja", "ko", "zh"}

    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        self.validate_request(request)
        
        # Read audio file
        with open(request.audio_path, "rb") as f:
            audio_data = f.read()
        
        params = {
            "model": self._model,
            "smart_format": "true",
            "punctuate": "true",
            "utterances": "true",
        }
        
        if request.language:
            params["language"] = request.language
        else:
            params["detect_language"] = "true"
        
        if request.diarization:
            params["diarize"] = "true"
        
        if request.word_alignments:
            params["words"] = "true"
        
        headers = {
            "Authorization": f"Token {self._api_key}",
            "Content-Type": "audio/wav",
        }
        
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                self._base_url,
                params=params,
                headers=headers,
                content=audio_data,
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse response
        channels = data.get("results", {}).get("channels", [])
        if not channels:
            raise RuntimeError("No transcription results from Deepgram")
        
        channel = channels[0]
        alternatives = channel.get("alternatives", [])
        if not alternatives:
            raise RuntimeError("No alternatives in Deepgram response")
        
        alt = alternatives[0]
        transcript = alt.get("transcript", "")
        words = alt.get("words", [])
        utterances = channel.get("utterances", [])
        
        # Build segments from utterances or words
        segments = []
        if utterances:
            for utt in utterances:
                start_ms = int(utt["start"] * 1000)
                end_ms = int(utt["end"] * 1000)
                text = utt["transcript"].strip()
                speaker = utt.get("speaker")
                
                # Find word alignments for this utterance
                alignments = None
                if request.word_alignments and words:
                    utt_words = [
                        w for w in words
                        if start_ms <= int(w["start"] * 1000) < end_ms
                    ]
                    if utt_words:
                        alignments = [
                            WordAlignment(
                                word=w["word"],
                                start_ms=int(w["start"] * 1000),
                                end_ms=int(w["end"] * 1000),
                                confidence=w.get("confidence", 0.0),
                            )
                            for w in utt_words
                        ]
                
                segments.append(SegmentResult(
                    start_ms=start_ms,
                    end_ms=end_ms,
                    text=text,
                    speaker=str(speaker) if speaker is not None else None,
                    confidence=utt.get("confidence"),
                    word_alignments=alignments,
                ))
        elif words:
            # Fallback: group words into segments
            current_segment = None
            for w in words:
                if current_segment is None or w["start"] - current_segment["end"] > 2.0:
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = {
                        "start": w["start"],
                        "end": w["end"],
                        "words": [w],
                    }
                else:
                    current_segment["end"] = w["end"]
                    current_segment["words"].append(w)
            
            if current_segment:
                segments.append(current_segment)
            
            # Convert to SegmentResult
            final_segments = []
            for seg in segments:
                alignments = None
                if request.word_alignments:
                    alignments = [
                        WordAlignment(
                            word=w["word"],
                            start_ms=int(w["start"] * 1000),
                            end_ms=int(w["end"] * 1000),
                            confidence=w.get("confidence", 0.0),
                        )
                        for w in seg["words"]
                    ]
                final_segments.append(SegmentResult(
                    start_ms=int(seg["start"] * 1000),
                    end_ms=int(seg["end"] * 1000),
                    text=" ".join(w["word"] for w in seg["words"]),
                    confidence=sum(w.get("confidence", 0) for w in seg["words"]) / len(seg["words"]),
                    word_alignments=alignments,
                ))
            segments = final_segments
        
        return TranscriptionResult(
            full_text=transcript,
            language=data.get("results", {}).get("channels", [{}])[0].get("detected_language", "en"),
            segments=segments,
            provider_metadata={
                "model": self.model_id,
                "request_id": data.get("metadata", {}).get("request_id"),
            },
        )


class GroqProvider(TranscriptionProvider):
    """Groq cloud transcription provider (Whisper)."""

    def __init__(self, api_key: str, model: str = "whisper-large-v3"):
        if not api_key:
            raise ValueError("Groq API key required")
        self._api_key = api_key
        self._model = model
        self._base_url = "https://api.groq.com/openai/v1/audio/transcriptions"

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_diarization(self) -> bool:
        return False

    @property
    def supports_word_alignments(self) -> bool:
        return False

    @property
    def supported_languages(self) -> Set[str]:
        return {"en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "ja", "ko", "zh", "ar", "hi"}

    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        self.validate_request(request)
        
        with open(request.audio_path, "rb") as f:
            files = {"file": (request.audio_path.name, f, "audio/wav")}
            data = {
                "model": self._model,
                "response_format": "verbose_json",
            }
            if request.language:
                data["language"] = request.language
            
            headers = {"Authorization": f"Bearer {self._api_key}"}
            
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    self._base_url,
                    headers=headers,
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                result = response.json()
        
        # Parse verbose_json response
        segments = []
        for seg in result.get("segments", []):
            segments.append(SegmentResult(
                start_ms=int(seg["start"] * 1000),
                end_ms=int(seg["end"] * 1000),
                text=seg["text"].strip(),
                confidence=seg.get("avg_logprob"),
            ))
        
        return TranscriptionResult(
            full_text=result.get("text", ""),
            language=result.get("language", request.language or "en"),
            segments=segments,
            provider_metadata={
                "model": self.model_id,
            },
        )


class OpenAIProvider(TranscriptionProvider):
    """OpenAI Whisper transcription provider."""

    def __init__(self, api_key: str, model: str = "whisper-1"):
        if not api_key:
            raise ValueError("OpenAI API key required")
        self._api_key = api_key
        self._model = model
        self._base_url = "https://api.openai.com/v1/audio/transcriptions"

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_diarization(self) -> bool:
        return False

    @property
    def supports_word_alignments(self) -> bool:
            return True

    @property
    def supported_languages(self) -> Set[str]:
        return {"en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru", "ja", "ko", "zh", "ar", "hi"}

    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        self.validate_request(request)
        
        with open(request.audio_path, "rb") as f:
            files = {"file": (request.audio_path.name, f, "audio/wav")}
            data = {
                "model": self._model,
                "response_format": "verbose_json",
            }
            if request.language:
                data["language"] = request.language
            
            headers = {"Authorization": f"Bearer {self._api_key}"}
            
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    self._base_url,
                    headers=headers,
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                result = response.json()
        
        # Parse verbose_json response
        segments = []
        for seg in result.get("segments", []):
            segments.append(SegmentResult(
                start_ms=int(seg["start"] * 1000),
                end_ms=int(seg["end"] * 1000),
                text=seg["text"].strip(),
                confidence=seg.get("avg_logprob"),
            ))
        
        return TranscriptionResult(
            full_text=result.get("text", ""),
            language=result.get("language", request.language or "en"),
            segments=segments,
            provider_metadata={
                "model": self.model_id,
            },
        )


class NvidiaNimProvider(TranscriptionProvider):
    """NVIDIA NIM self-hosted transcription provider."""

    def __init__(
        self,
        base_url: str,
        model: str = "parakeet-rnnt-1.1b",
        api_key: Optional[str] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._api_key = api_key

    @property
    def provider_name(self) -> str:
        return "nvidia_nim"

    @property
    def model_id(self) -> str:
        return self._model

    @property
    def supports_diarization(self) -> bool:
        return False  # Varies by model

    @property
    def supports_word_alignments(self) -> bool:
        return True  # Parakeet supports word timestamps

    @property
    def supported_languages(self) -> Set[str]:
        return {"en", "es", "fr", "de", "zh", "ja", "ko"}

    async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
        self.validate_request(request)
        
        with open(request.audio_path, "rb") as f:
            files = {"file": (request.audio_path.name, f, "audio/wav")}
            data = {
                "model": self._model,
            }
            if request.language:
                data["language"] = request.language
            if request.word_alignments:
                data["timestamp_granularities"] = "word"
            
            headers = {}
            if self._api_key:
                headers["Authorization"] = f"Bearer {self._api_key}"
            
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{self._base_url}/v1/audio/transcriptions",
                    headers=headers,
                    files=files,
                    data=data,
                )
                response.raise_for_status()
                result = response.json()
        
        # Parse response (OpenAI-compatible format)
        segments = []
        for seg in result.get("segments", []):
            alignments = None
            if request.word_alignments and "words" in seg:
                alignments = [
                    WordAlignment(
                        word=w["word"],
                        start_ms=int(w["start"] * 1000),
                        end_ms=int(w["end"] * 1000),
                        confidence=w.get("confidence", 0.0),
                    )
                    for w in seg["words"]
                ]
            
            segments.append(SegmentResult(
                start_ms=int(seg["start"] * 1000),
                end_ms=int(seg["end"] * 1000),
                text=seg["text"].strip(),
                confidence=seg.get("avg_logprob"),
                word_alignments=alignments,
            ))
        
        return TranscriptionResult(
            full_text=result.get("text", ""),
            language=result.get("language", request.language or "en"),
            segments=segments,
            provider_metadata={
                "model": self.model_id,
                "base_url": self._base_url,
            },
        )