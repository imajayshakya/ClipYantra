"""
Whisper Processor for ClipYantra.

Wrapper around faster-whisper for speech-to-text transcription
and speaker diarization using pyannote.audio.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from app.processors.base import (
    TranscriptionResult,
    TranscriptionSegment,
    DiarizationResult,
    DiarizationSegment,
    ProcessorError,
)


class WhisperProcessor:
    """
    High-level Whisper wrapper for transcription and diarization.
    
    Uses faster-whisper for efficient CPU/GPU inference
    and pyannote.audio for speaker diarization.
    """
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
        download_root: Optional[str] = None,
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.download_root = download_root
        
        self._model = None
        self._diarization_pipeline = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the Whisper model."""
        try:
            from faster_whisper import WhisperModel
            
            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                download_root=self.download_root,
            )
        except ImportError:
            raise ProcessorError(
                "faster-whisper not installed. Install with: pip install faster-whisper",
                code="MISSING_DEPENDENCY",
            )
        except Exception as e:
            raise ProcessorError(
                f"Failed to load Whisper model: {e}",
                code="MODEL_LOAD_ERROR",
            )
    
    def _load_diarization_pipeline(self) -> None:
        """Load the pyannote diarization pipeline."""
        if self._diarization_pipeline is not None:
            return
        
        try:
            from pyannote.audio import Pipeline
            from huggingface_hub import hf_hub_download
            
            # Use pyannote/speaker-diarization-3.1
            self._diarization_pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=os.environ.get("HUGGINGFACE_TOKEN"),
            )
            
            # Move to device
            import torch
            if self.device == "cuda" and torch.cuda.is_available():
                self._diarization_pipeline.to(torch.device("cuda"))
                
        except ImportError:
            raise ProcessorError(
                "pyannote.audio not installed. Install with: pip install pyannote.audio",
                code="MISSING_DEPENDENCY",
            )
        except Exception as e:
            raise ProcessorError(
                f"Failed to load diarization pipeline: {e}",
                code="DIARIZATION_LOAD_ERROR",
            )
    
    # =========================================================================
    # Transcription
    # =========================================================================
    
    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe",
        beam_size: int = 5,
        best_of: int = 5,
        patience: float = 1.0,
        temperature: Tuple[float, ...] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        compression_ratio_threshold: float = 2.4,
        log_prob_threshold: float = -1.0,
        no_speech_threshold: float = 0.6,
        condition_on_previous_text: bool = True,
        initial_prompt: Optional[str] = None,
        word_timestamps: bool = True,
        prepend_punctuations: str = "\"'\"¿([{-",
        append_punctuations: str = "\"'.。,，!！?？:：\")]}、",
    ) -> TranscriptionResult:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detect)
            task: "transcribe" or "translate"
            beam_size: Beam size for decoding
            best_of: Number of candidates for beam search
            patience: Patience for beam search
            temperature: Temperature for sampling
            compression_ratio_threshold: Compression ratio threshold
            log_prob_threshold: Log probability threshold
            no_speech_threshold: No speech threshold
            condition_on_previous_text: Condition on previous text
            initial_prompt: Initial prompt for decoding
            word_timestamps: Enable word-level timestamps
            prepend_punctuations: Punctuations to prepend
            append_punctuations: Punctuations to append
            
        Returns:
            TranscriptionResult with segments and metadata
        """
        if self._model is None:
            self._load_model()
        
        # Run transcription
        segments, info = self._model.transcribe(
            audio_path,
            language=language,
            task=task,
            beam_size=beam_size,
            best_of=best_of,
            patience=patience,
            temperature=temperature,
            compression_ratio_threshold=compression_ratio_threshold,
            log_prob_threshold=log_prob_threshold,
            no_speech_threshold=no_speech_threshold,
            condition_on_previous_text=condition_on_previous_text,
            initial_prompt=initial_prompt,
            word_timestamps=word_timestamps,
            prepend_punctuations=prepend_punctuations,
            append_punctuations=append_punctuations,
        )
        
        # Convert segments
        transcription_segments = []
        all_words = []
        full_text_parts = []
        
        for i, segment in enumerate(segments):
            words = []
            if segment.words:
                for word in segment.words:
                    word_dict = {
                        "word": word.word,
                        "start": word.start,
                        "end": word.end,
                        "probability": word.probability,
                    }
                    words.append(word_dict)
                    all_words.append(word_dict)
            
            trans_segment = TranscriptionSegment(
                id=i,
                start=segment.start,
                end=segment.end,
                text=segment.text.strip(),
                confidence=segment.avg_logprob,
                words=words,
            )
            transcription_segments.append(trans_segment)
            full_text_parts.append(segment.text.strip())
        
        return TranscriptionResult(
            text=" ".join(full_text_parts).strip(),
            language=info.language,
            language_probability=info.language_probability,
            duration=info.duration,
            segments=transcription_segments,
            words=all_words,
            model=self.model_size,
        )
    
    def transcribe_streaming(
        self,
        audio_path: str,
        chunk_length: int = 30,
        **transcribe_kwargs,
    ):
        """
        Transcribe with streaming/chunked processing for long files.
        
        Yields TranscriptionSegment as they're completed.
        """
        # For long files, split into chunks and process
        # This is a simplified version - full implementation would
        # handle overlapping chunks for continuity
        
        import subprocess
        
        # Get duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
            capture_output=True, text=True,
        )
        duration = float(result.stdout.strip())
        
        num_chunks = int(duration / chunk_length) + 1
        
        for chunk_idx in range(num_chunks):
            start = chunk_idx * chunk_length
            end = min(start + chunk_length, duration)
            
            # Extract chunk
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                chunk_path = tmp.name
            
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(start), "-t", str(end - start),
                "-i", audio_path, "-ar", "16000", "-ac", "1", chunk_path
            ], capture_output=True)
            
            # Transcribe chunk
            chunk_result = self.transcribe(chunk_path, **transcribe_kwargs)
            
            # Adjust timestamps
            for segment in chunk_result.segments:
                segment.start += start
                segment.end += start
                for word in segment.words:
                    word["start"] += start
                    word["end"] += start
            
            # Yield segments
            for segment in chunk_result.segments:
                yield segment
            
            # Cleanup
            Path(chunk_path).unlink(missing_ok=True)
    
    # =========================================================================
    # Speaker Diarization
    # =========================================================================
    
    def diarize(
        self,
        audio_path: str,
        max_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
        num_speakers: Optional[int] = None,
    ) -> DiarizationResult:
        """
        Perform speaker diarization on audio file.
        
        Args:
            audio_path: Path to audio file
            max_speakers: Maximum number of speakers
            min_speakers: Minimum number of speakers
            num_speakers: Exact number of speakers (if known)
            
        Returns:
            DiarizationResult with speaker segments
        """
        self._load_diarization_pipeline()
        
        # Run diarization
        diarization = self._diarization_pipeline(
            audio_path,
            num_speakers=num_speakers,
            min_speakers=min_speakers,
            max_speakers=max_speakers,
        )
        
        # Convert to our format
        segments = []
        speakers = set()
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append(DiarizationSegment(
                start=turn.start,
                end=turn.end,
                speaker=speaker,
            ))
            speakers.add(speaker)
        
        # Sort by start time
        segments.sort(key=lambda s: s.start)
        
        # Remap speaker labels to SPEAKER_00, SPEAKER_01, etc.
        speaker_map = {spk: f"SPEAKER_{i:02d}" for i, spk in enumerate(sorted(speakers))}
        for segment in segments:
            segment.speaker = speaker_map[segment.speaker]
        
        return DiarizationResult(
            segments=segments,
            speakers=sorted(speaker_map.values()),
            num_speakers=len(speakers),
        )
    
    def diarize_with_embeddings(
        self,
        audio_path: str,
        max_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
    ) -> Tuple[DiarizationResult, Dict[str, Any]]:
        """
        Perform diarization with speaker embeddings for identification.
        
        Returns:
            Tuple of (DiarizationResult, speaker_embeddings_dict)
        """
        # This would extract embeddings for each speaker
        # Useful for speaker identification across files
        diarization = self.diarize(audio_path, max_speakers, min_speakers)
        
        # Extract embeddings (placeholder - requires additional model)
        embeddings = {}
        # for speaker in diarization.speakers:
        #     embeddings[speaker] = self._extract_speaker_embedding(audio_path, speaker)
        
        return diarization, embeddings
    
    # =========================================================================
    # Combined Transcription + Diarization
    # =========================================================================
    
    def transcribe_and_diarize(
        self,
        audio_path: str,
        language: Optional[str] = None,
        max_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
    ) -> Tuple[TranscriptionResult, DiarizationResult]:
        """
        Run transcription and diarization in sequence.
        
        Returns:
            Tuple of (TranscriptionResult, DiarizationResult)
        """
        # Run transcription first
        transcription = self.transcribe(audio_path, language=language)
        
        # Run diarization
        diarization = self.diarize(
            audio_path,
            max_speakers=max_speakers,
            min_speakers=min_speakers,
        )
        
        return transcription, diarization
    
    # =========================================================================
    # Alignment
    # =========================================================================
    
    def align_transcription(
        self,
        transcription: TranscriptionResult,
        diarization: DiarizationResult,
    ) -> TranscriptionResult:
        """
        Align transcription segments with speaker diarization.
        
        Assigns speaker labels to transcription segments based on
        temporal overlap with diarization segments.
        """
        aligned_segments = []
        
        for t_segment in transcription.segments:
            t_start = t_segment.start
            t_end = t_segment.end
            t_mid = (t_start + t_end) / 2
            
            # Find best matching diarization segment
            best_speaker = "UNKNOWN"
            best_overlap = 0.0
            
            for d_segment in diarization.segments:
                overlap_start = max(t_start, d_segment.start)
                overlap_end = min(t_end, d_segment.end)
                overlap = max(0, overlap_end - overlap_start)
                
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = d_segment.speaker
            
            # Create aligned segment
            aligned_segment = TranscriptionSegment(
                id=t_segment.id,
                start=t_segment.start,
                end=t_segment.end,
                text=t_segment.text,
                confidence=t_segment.confidence,
                speaker=best_speaker,
                words=t_segment.words,
            )
            aligned_segments.append(aligned_segment)
        
        # Rebuild full text with speaker labels
        speaker_texts = {}
        for segment in aligned_segments:
            if segment.speaker not in speaker_texts:
                speaker_texts[segment.speaker] = []
            speaker_texts[segment.speaker].append(segment.text)
        
        # Combine text
        full_text = " ".join(segment.text for segment in aligned_segments)
        
        return TranscriptionResult(
            text=full_text,
            language=transcription.language,
            duration=transcription.duration,
            segments=aligned_segments,
            words=transcription.words,
            model=transcription.model,
        )
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        return [
            "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr",
            "pl", "ca", "nl", "ar", "sv", "it", "id", "hi", "fi", "vi",
            "he", "uk", "el", "ms", "cs", "ro", "da", "hu", "ta", "no",
            "th", "ur", "hr", "bg", "lt", "la", "mi", "ml", "cy", "sk",
            "te", "fa", "lv", "bn", "sr", "az", "sl", "kn", "et", "mk",
            "br", "eu", "is", "hy", "ne", "mn", "bs", "kk", "sq", "sw",
            "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc",
            "ka", "be", "tg", "sd", "gu", "am", "yi", "lo", "uz", "fo",
            "ht", "ps", "tk", "nn", "mt", "sa", "lb", "my", "bo", "tl",
            "mg", "as", "tt", "haw", "ln", "ha", "ba", "jw", "su",
        ]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_size": self.model_size,
            "device": self.device,
            "compute_type": self.compute_type,
            "download_root": self.download_root,
        }
    
    @staticmethod
    def get_available_models() -> List[str]:
        """Get list of available Whisper model sizes."""
        return ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
    
    @staticmethod
    def estimate_vram_usage(model_size: str, device: str = "cuda") -> Dict[str, int]:
        """Estimate VRAM usage for model on GPU."""
        # Approximate VRAM requirements in MB
        vram_estimates = {
            "tiny": {"int8": 1000, "float16": 1500, "float32": 2000},
            "base": {"int8": 1500, "float16": 2000, "float32": 3000},
            "small": {"int8": 2500, "float16": 3500, "float32": 5000},
            "medium": {"int8": 5000, "float16": 7000, "float32": 10000},
            "large": {"int8": 10000, "float16": 14000, "float32": 20000},
            "large-v2": {"int8": 10000, "float16": 14000, "float32": 20000},
            "large-v3": {"int8": 10000, "float16": 14000, "float32": 20000},
        }
        
        if device == "cpu":
            return {"ram_mb": vram_estimates.get(model_size, {}).get("float32", 0) // 2}
        
        compute_types = ["int8", "float16", "float32"]
        result = {}
        for ct in compute_types:
            if model_size in vram_estimates and ct in vram_estimates[model_size]:
                result[f"vram_mb_{ct}"] = vram_estimates[model_size][ct]
        return result