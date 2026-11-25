"""
Unit tests for Whisper processor.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from app.processors.whisper_processor import WhisperProcessor
from app.processors.base import TranscriptionResult, TranscriptionSegment, DiarizationResult, SpeakerSegment


class TestWhisperProcessor:
    """Tests for WhisperProcessor."""

    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return WhisperProcessor(
            model_size="tiny",
            device="cpu",
            compute_type="int8"
        )

    @pytest.fixture
    def mock_transcription_result(self):
        """Mock transcription result from faster-whisper."""
        mock_segment1 = MagicMock()
        mock_segment1.id = 0
        mock_segment1.start = 0.0
        mock_segment1.end = 5.0
        mock_segment1.text = "Hello world."
        mock_segment1.words = [
            MagicMock(word="Hello", start=0.0, end=0.5, probability=0.99),
            MagicMock(word="world", start=0.5, end=1.0, probability=0.98)
        ]
        mock_segment1.avg_logprob = -0.1
        mock_segment1.compression_ratio = 1.5
        mock_segment1.no_speech_prob = 0.01

        mock_segment2 = MagicMock()
        mock_segment2.id = 1
        mock_segment2.start = 5.0
        mock_segment2.end = 10.0
        mock_segment2.text = "This is a test."
        mock_segment2.words = [
            MagicMock(word="This", start=5.0, end=5.2, probability=0.99),
            MagicMock(word="is", start=5.2, end=5.3, probability=0.99),
            MagicMock(word="a", start=5.3, end=5.4, probability=0.99),
            MagicMock(word="test", start=5.4, end=5.7, probability=0.98)
        ]
        mock_segment2.avg_logprob = -0.2
        mock_segment2.compression_ratio = 1.4
        mock_segment2.no_speech_prob = 0.02

        mock_info = MagicMock()
        mock_info.language = "en"
        mock_info.language_probability = 0.99
        mock_info.duration = 10.0

        return ([mock_segment1, mock_segment2], mock_info)

    @pytest.mark.asyncio
    async def test_transcribe(self, processor, mock_transcription_result):
        """Test basic transcription."""
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.return_value = mock_transcription_result
                
                result = await processor.transcribe(
                    "/test/audio.wav",
                    language="en",
                    task="transcribe"
                )
                
                assert isinstance(result, TranscriptionResult)
                assert result.text == "Hello world. This is a test."
                assert result.language == "en"
                assert result.language_probability == 0.99
                assert result.duration == 10.0
                assert len(result.segments) == 2
                
                # Check first segment
                seg1 = result.segments[0]
                assert seg1.id == 0
                assert seg1.start == 0.0
                assert seg1.end == 5.0
                assert seg1.text == "Hello world."
                assert len(seg1.words) == 2
                
                # Check second segment
                seg2 = result.segments[1]
                assert seg2.id == 1
                assert seg2.start == 5.0
                assert seg2.end == 10.0
                assert seg2.text == "This is a test."
                assert len(seg2.words) == 4

    @pytest.mark.asyncio
    async def test_transcribe_with_word_timestamps(self, processor, mock_transcription_result):
        """Test transcription with word-level timestamps."""
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.return_value = mock_transcription_result
                
                result = await processor.transcribe(
                    "/test/audio.wav",
                    language="en",
                    word_timestamps=True
                )
                
                assert len(result.word_timestamps) == 6  # 2 + 4 words
                assert result.word_timestamps[0]["word"] == "Hello"
                assert result.word_timestamps[0]["start"] == 0.0
                assert result.word_timestamps[0]["end"] == 0.5
                assert result.word_timestamps[2]["word"] == "This"
                assert result.word_timestamps[5]["word"] == "test"

    @pytest.mark.asyncio
    async def test_transcribe_with_vad(self, processor, mock_transcription_result):
        """Test transcription with voice activity detection."""
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.return_value = mock_transcription_result
                
                result = await processor.transcribe(
                    "/test/audio.wav",
                    vad_filter=True,
                    vad_parameters={"min_silence_duration_ms": 500}
                )
                
                assert isinstance(result, TranscriptionResult)
                mock_transcribe.assert_called_once()
                call_kwargs = mock_transcribe.call_args[1]
                assert call_kwargs["vad_filter"] is True
                assert "vad_parameters" in call_kwargs

    @pytest.mark.asyncio
    async def test_transcribe_translation(self, processor):
        """Test transcription with translation."""
        mock_translate_result = (
            [
                MagicMock(
                    id=0, start=0.0, end=5.0, text="Hello world.",
                    words=[MagicMock(word="Hello", start=0.0, end=0.5, probability=0.99)],
                    avg_logprob=-0.1, compression_ratio=1.5, no_speech_prob=0.01
                )
            ],
            MagicMock(language="es", language_probability=0.95, duration=5.0)
        )
        
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.return_value = mock_translate_result
                
                result = await processor.transcribe(
                    "/test/audio.wav",
                    language="es",
                    task="translate"
                )
                
                assert result.text == "Hello world."
                assert result.language == "es"
                mock_transcribe.assert_called_once()
                call_kwargs = mock_transcribe.call_args[1]
                assert call_kwargs["task"] == "translate"

    @pytest.mark.asyncio
    async def test_diarize(self, processor):
        """Test speaker diarization."""
        # Mock pyannote pipeline output
        mock_diarization = MagicMock()
        mock_diarization.itertracks.return_value = [
            (MagicMock(start=0.0, end=5.0), _, "SPEAKER_00"),
            (MagicMock(start=5.0, end=10.0), _, "SPEAKER_01"),
            (MagicMock(start=10.0, end=15.0), _, "SPEAKER_00"),
        ]
        
        with patch.object(processor, '_load_diarization_pipeline', new_callable=AsyncMock):
            with patch.object(processor.diarization_pipeline, '__call__', return_value=mock_diarization):
                result = await processor.diarize("/test/audio.wav")
                
                assert isinstance(result, DiarizationResult)
                assert len(result.speakers) == 3
                assert result.speakers[0].speaker == "SPEAKER_00"
                assert result.speakers[0].start == 0.0
                assert result.speakers[0].end == 5.0
                assert result.speakers[1].speaker == "SPEAKER_01"
                assert result.speakers[2].speaker == "SPEAKER_00"
                assert result.num_speakers == 2

    @pytest.mark.asyncio
    async def test_transcribe_with_diarization(self, processor, mock_transcription_result):
        """Test transcription with speaker diarization."""
        mock_diarization = MagicMock()
        mock_diarization.itertracks.return_value = [
            (MagicMock(start=0.0, end=5.0), _, "SPEAKER_00"),
            (MagicMock(start=5.0, end=10.0), _, "SPEAKER_01"),
        ]
        
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                with patch.object(processor, '_load_diarization_pipeline', new_callable=AsyncMock):
                    with patch.object(processor.diarization_pipeline, '__call__', return_value=mock_diarization):
                        mock_transcribe.return_value = mock_transcription_result
                        
                        result = await processor.transcribe_with_diarization(
                            "/test/audio.wav",
                            diarization_model="pyannote/speaker-diarization-3.1",
                            auth_token="test_token"
                        )
                        
                        assert isinstance(result, TranscriptionResult)
                        assert len(result.diarization) == 2
                        assert result.diarization[0]["speaker"] == "SPEAKER_00"
                        assert result.diarization[1]["speaker"] == "SPEAKER_01"

    @pytest.mark.asyncio
    async def test_align_transcription(self, processor, mock_transcription_result):
        """Test transcription alignment (word-level timestamps)."""
        # Create a transcription result without word timestamps
        transcription = TranscriptionResult(
            text="Hello world. This is a test.",
            language="en",
            language_probability=0.99,
            duration=10.0,
            segments=[
                TranscriptionSegment(
                    id=0, start=0.0, end=5.0, text="Hello world.",
                    words=[], avg_logprob=-0.1, compression_ratio=1.5, no_speech_prob=0.01
                ),
                TranscriptionSegment(
                    id=1, start=5.0, end=10.0, text="This is a test.",
                    words=[], avg_logprob=-0.2, compression_ratio=1.4, no_speech_prob=0.02
                )
            ]
        )
        
        # Mock aligned result
        mock_aligned_result = (
            [
                MagicMock(
                    id=0, start=0.0, end=5.0, text="Hello world.",
                    words=[
                        MagicMock(word="Hello", start=0.0, end=0.5, probability=0.99),
                        MagicMock(word="world", start=0.5, end=1.0, probability=0.98)
                    ],
                    avg_logprob=-0.1, compression_ratio=1.5, no_speech_prob=0.01
                ),
                MagicMock(
                    id=1, start=5.0, end=10.0, text="This is a test.",
                    words=[
                        MagicMock(word="This", start=5.0, end=5.2, probability=0.99),
                        MagicMock(word="is", start=5.2, end=5.3, probability=0.99),
                        MagicMock(word="a", start=5.3, end=5.4, probability=0.99),
                        MagicMock(word="test", start=5.4, end=5.7, probability=0.98)
                    ],
                    avg_logprob=-0.2, compression_ratio=1.4, no_speech_prob=0.02
                )
            ],
            MagicMock(language="en", language_probability=0.99, duration=10.0)
        )
        
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.return_value = mock_aligned_result
                
                result = await processor.align_transcription("/test/audio.wav", transcription)
                
                assert len(result.segments[0].words) == 2
                assert len(result.segments[1].words) == 4
                assert len(result.word_timestamps) == 6

    @pytest.mark.asyncio
    async def test_load_model_caching(self, processor):
        """Test that model is cached after loading."""
        with patch('faster_whisper.WhisperModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            
            # First load
            await processor._load_model()
            assert processor.model is mock_model
            mock_model_class.assert_called_once()
            
            # Second load should use cache
            mock_model_class.reset_mock()
            await processor._load_model()
            mock_model_class.assert_not_called()

    @pytest.mark.asyncio
    async def test_load_diarization_pipeline_caching(self, processor):
        """Test that diarization pipeline is cached."""
        with patch('pyannote.audio.Pipeline.from_pretrained') as mock_pipeline:
            mock_pipeline_instance = MagicMock()
            mock_pipeline.return_value = mock_pipeline_instance
            
            # First load
            await processor._load_diarization_pipeline("test_model", "test_token")
            assert processor.diarization_pipeline is mock_pipeline_instance
            mock_pipeline.assert_called_once()
            
            # Second load should use cache
            mock_pipeline.reset_mock()
            await processor._load_diarization_pipeline("test_model", "test_token")
            mock_pipeline.assert_not_called()

    @pytest.mark.asyncio
    async def test_transcribe_error_handling(self, processor):
        """Test error handling in transcription."""
        with patch.object(processor, '_load_model', new_callable=AsyncMock):
            with patch.object(processor.model, 'transcribe', new_callable=AsyncMock) as mock_transcribe:
                mock_transcribe.side_effect = RuntimeError("Model inference failed")
                
                with pytest.raises(RuntimeError) as exc_info:
                    await processor.transcribe("/test/audio.wav")
                
                assert "Model inference failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_diarize_error_handling(self, processor):
        """Test error handling in diarization."""
        with patch.object(processor, '_load_diarization_pipeline', new_callable=AsyncMock):
            with patch.object(processor.diarization_pipeline, '__call__', side_effect=RuntimeError("Diarization failed")):
                with pytest.raises(RuntimeError) as exc_info:
                    await processor.diarize("/test/audio.wav")
                
                assert "Diarization failed" in str(exc_info.value)

    def test_get_supported_languages(self, processor):
        """Test getting supported languages."""
        languages = processor.get_supported_languages()
        
        assert isinstance(languages, list)
        assert "en" in languages
        assert "es" in languages
        assert "fr" in languages
        assert "de" in languages
        assert len(languages) > 50

    def test_get_available_models(self, processor):
        """Test getting available models."""
        models = processor.get_available_models()
        
        assert isinstance(models, list)
        assert "tiny" in models
        assert "base" in models
        assert "small" in models
        assert "medium" in models
        assert "large-v3" in models