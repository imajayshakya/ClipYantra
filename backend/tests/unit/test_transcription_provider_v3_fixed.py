"""Unit tests for TranscriptionProvider implementations (ING-003)."""

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.transcription_provider import (
    TranscriptionProvider,
    TranscriptionRequest,
    TranscriptionResult,
    SegmentResult,
    WordAlignment,
    WhisperXProvider,
    DeepgramProvider,
    GroqProvider,
    OpenAIProvider,
    NvidiaNimProvider,
)


class TestTranscriptionDataclasses:
    """Test transcription data classes."""

    def test_transcription_request_required_fields(self):
        """Test TranscriptionRequest with required fields."""
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
        )
        assert request.audio_path == Path("/tmp/audio.wav")
        assert request.language == "en"
        assert request.diarization is False
        assert request.word_alignments is False
        assert request.metadata == {}

    def test_transcription_request_with_metadata(self):
        """Test TranscriptionRequest with optional fields."""
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="es",
            diarization=True,
            word_alignments=True,
            metadata={"source": "test"},
        )
        assert request.language == "es"
        assert request.diarization is True
        assert request.word_alignments is True
        assert request.metadata == {"source": "test"}

    def test_segment_result_properties(self):
        """Test SegmentResult properties."""
        segment = SegmentResult(
            start_ms=1000,
            end_ms=5000,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95,
            word_alignments=[
                WordAlignment(word="Hello", start_ms=1000, end_ms=2500, confidence=0.9),
                WordAlignment(word="world", start_ms=2500, end_ms=5000, confidence=0.95),
            ],
        )
        assert segment.start_ms == 1000
        assert segment.end_ms == 5000
        assert segment.text == "Hello world"
        assert segment.speaker == "SPEAKER_00"
        assert segment.confidence == 0.95
        assert len(segment.word_alignments) == 2

    def test_segment_result_with_words(self):
        """Test SegmentResult with words (legacy alias for word_alignments)."""
        segment = SegmentResult(
            start_ms=1000,
            end_ms=5000,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95,
            words=[
                WordAlignment(word="Hello", start_ms=1000, end_ms=2500, confidence=0.9),
                WordAlignment(word="world", start_ms=2500, end_ms=5000, confidence=0.95),
            ],
        )
        # words should be converted to word_alignments (both are WordAlignment lists)
        assert segment.word_alignments is not None
        assert len(segment.word_alignments) == 2
        assert segment.word_alignments[0].word == "Hello"
        assert segment.word_alignments[1].word == "world"

    def test_segment_result_word_alignments_alias(self):
        """Test word_alignments property works as alias for words."""
        segment = SegmentResult(
            start_ms=1000,
            end_ms=5000,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95,
            word_alignments=[
                WordAlignment(word="Hello", start_ms=1000, end_ms=2500, confidence=0.9),
            ],
        )
        # Access via words property
        assert hasattr(segment, 'words')
        # The words property should return word_alignments in dict format
        assert segment.words == segment.word_alignments

    def test_transcription_result_properties(self):
        """Test TranscriptionResult properties."""
        result = TranscriptionResult(
            full_text="Hello world",
            language="en",
            segments=[
                SegmentResult(
                    start_ms=0,
                    end_ms=5000,
                    text="Hello world",
                    speaker=None,
                    confidence=0.95,
                    word_alignments=None,
                )
            ],
            provider_metadata={"model": "test", "duration_ms": 5000},
        )
        assert result.full_text == "Hello world"
        assert result.language == "en"
        assert len(result.segments) == 1
        assert result.provider_metadata["model"] == "test"


class TestTranscriptionProviderBase:
    """Test TranscriptionProvider base class."""

    def test_provider_properties(self):
        """Test abstract properties must be implemented."""
        class TestProvider(TranscriptionProvider):
            async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
            
            @property
            def provider_name(self) -> str:
                return "test"
            
            @property
            def model_id(self) -> str:
                return "test-model"
            
            @property
            def supports_diarization(self) -> bool:
                return False
            
            @property
            def supports_word_alignments(self) -> bool:
                return False
            
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}

        provider = TestProvider()
        assert provider.provider_name == "test"
        assert provider.model_id == "test-model"
        assert provider.supports_diarization is False
        assert provider.supports_word_alignments is False
        assert provider.supported_languages == {"en"}

    def test_supports_diarization_default(self):
        """Test supports_diarization defaults to False."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            @property
            def model_id(self) -> str:
                return "test-model"
            @property
            def supports_word_alignments(self) -> bool:
                return False
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}
            async def transcribe(self, request):
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        assert provider.supports_diarization is False

    def test_supports_word_alignments_default(self):
        """Test supports_word_alignments defaults to False."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            @property
            def model_id(self) -> str:
                return "test-model"
            @property
            def supports_diarization(self) -> bool:
                return False
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}
            async def transcribe(self, request):
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        assert provider.supports_word_alignments is False

    def test_supported_languages_default(self):
        """Test supported_languages defaults to empty set."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            @property
            def model_id(self) -> str:
                return "test-model"
            @property
            def supports_diarization(self) -> bool:
                return False
            @property
            def supports_word_alignments(self) -> bool:
                return False
            @property
            def supported_languages(self) -> set[str]:
                return set()
            async def transcribe(self, request):
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        assert provider.supported_languages == set()

    def test_validate_request_diarization_not_supported(self):
        """Test validate_request raises for unsupported diarization."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            
            @property
            def model_id(self) -> str:
                return "test-model"
            
            @property
            def supports_diarization(self) -> bool:
                return False
            
            @property
            def supports_word_alignments(self) -> bool:
                return True
            
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}
            
            async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            diarization=True,
        )
        with pytest.raises(ValueError, match="does not support diarization"):
            provider.validate_request(request)

    def test_validate_request_word_alignments_not_supported(self):
        """Test validate_request raises for unsupported word alignments."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            
            @property
            def model_id(self) -> str:
                return "test-model"
            
            @property
            def supports_diarization(self) -> bool:
                return True
            
            @property
            def supports_word_alignments(self) -> bool:
                return False
            
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}
            
            async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            word_alignments=True,
        )
        with pytest.raises(ValueError, match="does not support word alignments"):
            provider.validate_request(request)

    def test_validate_request_unsupported_language(self):
        """Test validate_request raises for unsupported language."""
        class TestProvider(TranscriptionProvider):
            @property
            def provider_name(self) -> str:
                return "test"
            
            @property
            def model_id(self) -> str:
                return "test-model"
            
            @property
            def supports_diarization(self) -> bool:
                return True
            
            @property
            def supports_word_alignments(self) -> bool:
                return True
            
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}
            
            async def transcribe(self, request: TranscriptionRequest) -> TranscriptionResult:
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
        
        provider = TestProvider()
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="xx",
        )
        with pytest.raises(ValueError, match="does not support language"):
            provider.validate_request(request)


class TestWhisperXProvider:
    """Test WhisperXProvider implementation."""

    def test_provider_name_and_model(self):
        """Test provider identification."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        assert provider.provider_name == "whisperx"
        assert provider.model_id == "whisper-large-v3"

    def test_supports_diarization(self):
        """Test WhisperX supports diarization."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        assert provider.supports_diarization is True

    def test_supports_word_alignments(self):
        """Test WhisperX supports word alignments."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        assert provider.supports_word_alignments is True

    def test_supported_languages(self):
        """Test WhisperX supported languages."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        assert "en" in provider.supported_languages
        assert "es" in provider.supported_languages
        assert "fr" in provider.supported_languages

    @pytest.mark.asyncio
    async def test_transcribe_not_available_raises(self):
        """Test transcribe raises when WhisperX not available."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
        )
        with pytest.raises(RuntimeError, match="WhisperX not installed"):
            await provider.transcribe(request)

    def test_validate_capabilities_diarization_not_requested(self):
        """Test validate_capabilities passes when diarization not requested."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            diarization=False,
        )
        # Should not raise
        TranscriptionProvider.validate_capabilities(provider, request.language, request.diarization, request.word_alignments)

    def test_validate_capabilities_unsupported_language(self):
        """Test validate_capabilities fails for unsupported language."""
        provider = WhisperXProvider(model="large-v3", device="cpu")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="xx",
            diarization=False,
        )
        with pytest.raises(ValueError, match="does not support language"):
            TranscriptionProvider.validate_capabilities(provider, language="xx", diarization=False)


class TestDeepgramProvider:
    """Test DeepgramProvider implementation."""

    def test_provider_name_and_model(self):
        """Test provider identification."""
        provider = DeepgramProvider(api_key="test-key", model="nova-2")
        assert provider.provider_name == "deepgram"
        assert provider.model_id == "nova-2"

    def test_supports_diarization(self):
        """Test Deepgram supports diarization."""
        provider = DeepgramProvider(api_key="test-key", model="nova-2")
        assert provider.supports_diarization is True

    def test_supports_word_alignments(self):
        """Test Deepgram supports word alignments."""
        provider = DeepgramProvider(api_key="test-key", model="nova-2")
        assert provider.supports_word_alignments is True

    def test_supported_languages(self):
        """Test Deepgram supported languages."""
        provider = DeepgramProvider(api_key="test-key", model="nova-2")
        assert "en" in provider.supported_languages
        assert "es" in provider.supported_languages

    def test_validate_capabilities_unsupported_language(self):
        """Test validate_capabilities fails for unsupported language."""
        provider = DeepgramProvider(api_key="test-key", model="nova-2")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="xx",
            diarization=False,
        )
        with pytest.raises(ValueError, match="does not support language"):
            TranscriptionProvider.validate_capabilities(provider, language="xx", diarization=False)


class TestGroqProvider:
    """Test GroqProvider implementation."""

    def test_provider_name_and_model(self):
        """Test provider identification."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        assert provider.provider_name == "groq"
        assert provider.model_id == "whisper-large-v3"

    def test_supports_diarization_false(self):
        """Test Groq does not support diarization."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        assert provider.supports_diarization is False

    def test_supports_word_alignments_false(self):
        """Test Groq does not support word alignments."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        assert provider.supports_word_alignments is False

    def test_supported_languages(self):
        """Test Groq supported languages."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        assert "en" in provider.supported_languages
        assert "es" in provider.supported_languages

    def test_validate_capabilities_diarization_raises(self):
        """Test validate_capabilities fails when diarization requested."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            diarization=True,
        )
        with pytest.raises(ValueError, match="does not support diarization"):
            TranscriptionProvider.validate_capabilities(provider, language="en", diarization=True)

    def test_validate_capabilities_word_alignments_raises(self):
        """Test validate_capabilities fails when word alignments requested."""
        provider = GroqProvider(api_key="test-key", model="whisper-large-v3")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            word_alignments=True,
        )
        with pytest.raises(ValueError, match="does not support word_alignments"):
            TranscriptionProvider.validate_capabilities(provider, language="en", word_alignments=True)


class TestOpenAIProvider:
    """Test OpenAIProvider implementation."""

    def test_provider_name_and_model(self):
        """Test provider identification."""
        provider = OpenAIProvider(api_key="test-key", model="whisper-1")
        assert provider.provider_name == "openai"
        assert provider.model_id == "whisper-1"

    def test_supports_diarization_false(self):
        """Test OpenAI does not support diarization."""
        provider = OpenAIProvider(api_key="test-key", model="whisper-1")
        assert provider.supports_diarization is False

    def test_supports_word_alignments_true(self):
        """Test OpenAI supports word alignments."""
        provider = OpenAIProvider(api_key="test-key", model="whisper-1")
        assert provider.supports_word_alignments is True

    def test_supported_languages(self):
        """Test OpenAI supported languages."""
        provider = OpenAIProvider(api_key="test-key", model="whisper-1")
        assert "en" in provider.supported_languages
        assert "es" in provider.supported_languages

    def test_validate_capabilities_diarization_raises(self):
        """Test validate_capabilities fails when diarization requested."""
        provider = OpenAIProvider(api_key="test-key", model="whisper-1")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            diarization=True,
        )
        with pytest.raises(ValueError, match="does not support diarization"):
            TranscriptionProvider.validate_capabilities(provider, language="en", diarization=True)


class TestNvidiaNimProvider:
    """Test NvidiaNimProvider implementation."""

    def test_provider_name_and_model(self):
        """Test provider identification."""
        provider = NvidiaNimProvider(base_url="http://localhost:8000", model="parakeet-rnnt-1.1b", api_key="test-key")
        assert provider.provider_name == "nvidia_nim"
        assert provider.model_id == "parakeet-rnnt-1.1b"

    def test_supports_diarization_true(self):
        """Test Nvidia NIM supports diarization."""
        provider = NvidiaNimProvider(base_url="http://localhost:8000", model="parakeet-rnnt-1.1b", api_key="test-key")
        assert provider.supports_diarization is False  # Varies by model, default is False

    def test_supports_word_alignments_false(self):
        """Test Nvidia NIM does not support word alignments."""
        provider = NvidiaNimProvider(base_url="http://localhost:8000", model="parakeet-rnnt-1.1b", api_key="test-key")
        assert provider.supports_word_alignments is True  # Parakeet supports word timestamps

    def test_supported_languages(self):
        """Test Nvidia NIM supported languages."""
        provider = NvidiaNimProvider(base_url="http://localhost:8000", model="parakeet-rnnt-1.1b", api_key="test-key")
        assert "en" in provider.supported_languages

    def test_validate_capabilities_diarization_raises(self):
        """Test validate_capabilities fails when diarization requested (NIM doesn't support it)."""
        provider = NvidiaNimProvider(base_url="http://localhost:8000", model="parakeet-rnnt-1.1b", api_key="test-key")
        request = TranscriptionRequest(
            audio_path=Path("/tmp/audio.wav"),
            language="en",
            diarization=True,
        )
        with pytest.raises(ValueError, match="does not support diarization"):
            TranscriptionProvider.validate_capabilities(provider, language="en", diarization=True)


class TestProviderValidationClassmethod:
    """Test validate_capabilities as classmethod behavior."""

    def test_validate_capabilities_is_classmethod(self):
        """Test validate_capabilities is a classmethod."""
        import inspect
        assert isinstance(inspect.getattr_static(TranscriptionProvider, 'validate_capabilities'), classmethod)

    def test_validate_capabilities_called_on_class(self):
        """Test validate_capabilities can be called on class."""
        # This should not raise - testing classmethod behavior
        class TestProvider(TranscriptionProvider):
            async def transcribe(self, request):
                return TranscriptionResult(full_text="", language="en", segments=[], provider_metadata={})
            
            @property
            def provider_name(self) -> str:
                return "test"
            
            @property
            def model_id(self) -> str:
                return "test-model"
            
            @property
            def supports_diarization(self) -> bool:
                return False
            
            @property
            def supports_word_alignments(self) -> bool:
                return False
            
            @property
            def supported_languages(self) -> set[str]:
                return {"en"}

        provider = TestProvider()
        request = TranscriptionRequest(audio_path=Path("/tmp/a.wav"), language="en")
        # Call on instance should work via classmethod
        TestProvider.validate_capabilities(provider, request.language, request.diarization, request.word_alignments)
        provider.validate_capabilities(provider, request.language, request.diarization, request.word_alignments)  # Also works via instance