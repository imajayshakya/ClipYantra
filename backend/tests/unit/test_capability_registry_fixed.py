"""Unit tests for CapabilityRegistry (ING-003)."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from app.services.capability_registry import (
    CapabilityRegistry,
    RoutingPolicy,
    ProviderCapability,
    create_capability_registry,
)


class TestCapabilityRegistry:
    """Test CapabilityRegistry functionality."""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings object."""
        settings = Mock()
        settings.TRANSCRIPTION_ROUTING_POLICY = "local_first"
        settings.WHISPERX_MODEL = "large-v3"
        settings.WHISPERX_DEVICE = "cpu"
        settings.DEEPGRAM_API_KEY = "test_deepgram_key"
        settings.DEEPGRAM_MODEL = "nova-2"
        settings.GROQ_API_KEY = "test_groq_key"
        settings.GROQ_MODEL = "whisper-large-v3"
        settings.OPENAI_API_KEY = "test_openai_key"
        settings.OPENAI_WHISPER_MODEL = "whisper-1"
        settings.NVIDIA_NIM_BASE_URL = None
        settings.NVIDIA_NIM_MODEL = "parakeet-rnnt-1.1b"
        settings.NVIDIA_NIM_API_KEY = None
        return settings

    @pytest.fixture
    def registry(self, mock_settings):
        """Create registry with mocked providers."""
        with patch("app.services.capability_registry.WhisperXProvider") as mock_whisperx, \
             patch("app.services.capability_registry.DeepgramProvider") as mock_deepgram, \
             patch("app.services.capability_registry.GroqProvider") as mock_groq, \
             patch("app.services.capability_registry.OpenAIProvider") as mock_openai:
            
            # Configure mock providers
            mock_whisperx_instance = Mock()
            mock_whisperx_instance.provider_name = "whisperx"
            mock_whisperx_instance.model_id = "large-v3"
            mock_whisperx_instance.supports_diarization = True
            mock_whisperx_instance.supports_word_alignments = True
            mock_whisperx_instance.supported_languages = {"en", "es", "hi", "fr", "de"}
            mock_whisperx.return_value = mock_whisperx_instance
            
            mock_deepgram_instance = Mock()
            mock_deepgram_instance.provider_name = "deepgram"
            mock_deepgram_instance.model_id = "nova-2"
            mock_deepgram_instance.supports_diarization = True
            mock_deepgram_instance.supports_word_alignments = True
            mock_deepgram_instance.supported_languages = {"en", "es", "fr", "de", "it", "pt"}
            mock_deepgram.return_value = mock_deepgram_instance
            
            mock_groq_instance = Mock()
            mock_groq_instance.provider_name = "groq"
            mock_groq_instance.model_id = "whisper-large-v3"
            mock_groq_instance.supports_diarization = False
            mock_groq_instance.supports_word_alignments = False
            mock_groq_instance.supported_languages = {"en", "es", "fr", "de", "it", "pt", "hi", "ja", "ko", "zh"}
            mock_groq.return_value = mock_groq_instance
            
            mock_openai_instance = Mock()
            mock_openai_instance.provider_name = "openai"
            mock_openai_instance.model_id = "whisper-1"
            mock_openai_instance.supports_diarization = False
            mock_openai_instance.supports_word_alignments = False
            mock_openai_instance.supported_languages = {"en", "es", "fr", "de", "it", "pt", "hi", "ja", "ko", "zh"}
            mock_openai.return_value = mock_openai_instance
            
            registry = CapabilityRegistry(
                policy=RoutingPolicy.LOCAL_FIRST,
                whisperx_model="large-v3",
                whisperx_device="cpu",
                deepgram_api_key="test_deepgram_key",
                deepgram_model="nova-2",
                groq_api_key="test_groq_key",
                groq_model="whisper-large-v3",
                openai_api_key="test_openai_key",
                openai_model="whisper-1",
                nvidia_nim_base_url=None,
            )
            
            return registry

    def test_registry_initializes_all_providers(self, registry):
        """Test registry initializes all available providers."""
        providers = registry.list_providers()
        provider_names = [p.provider_name for p in providers]
        
        assert "whisperx" in provider_names
        assert "deepgram" in provider_names
        assert "groq" in provider_names
        assert "openai" in provider_names
        assert len(providers) == 4

    def test_get_transcription_provider_explicit_hint(self, registry):
        """Test explicit provider hint is respected."""
        provider = registry.get_transcription_provider(hint="deepgram")
        assert provider.provider_name == "deepgram"

    def test_get_transcription_provider_invalid_hint_raises(self, registry):
        """Test invalid provider hint raises ValueError."""
        with pytest.raises(ValueError, match="Provider 'invalid' not available"):
            registry.get_transcription_provider(hint="invalid")

    def test_get_transcription_provider_diarization_requirement(self, registry):
        """Test provider selection respects diarization requirement."""
        # WhisperX and Deepgram support diarization
        provider = registry.get_transcription_provider(diarization=True)
        assert provider.provider_name in ("whisperx", "deepgram")
        assert provider.supports_diarization is True

    def test_get_transcription_provider_word_alignments_requirement(self, registry):
        """Test provider selection respects word_alignments requirement."""
        provider = registry.get_transcription_provider(word_alignments=True)
        assert provider.provider_name in ("whisperx", "deepgram")
        assert provider.supports_word_alignments is True

    def test_get_transcription_provider_language_requirement(self, registry):
        """Test provider selection respects language requirement."""
        # All providers support English
        provider = registry.get_transcription_provider(language="en")
        assert "en" in provider.supported_languages
        
        # Test language only some providers support
        provider = registry.get_transcription_provider(language="hi")
        assert "hi" in provider.supported_languages

    def test_get_transcription_provider_no_match_raises(self, registry):
        """Test no matching provider raises ValueError."""
        # Request diarization + word_alignments + unsupported language
        with pytest.raises(ValueError, match="No provider available"):
            registry.get_transcription_provider(
                diarization=True,
                word_alignments=True,
                language="xx"  # Unsupported language
            )

    def test_routing_policy_local_first(self, registry):
        """Test LOCAL_FIRST policy prefers WhisperX."""
        # With diarization required, both whisperx and deepgram qualify
        # LOCAL_FIRST should prefer whisperx
        provider = registry.get_transcription_provider(diarization=True)
        assert provider.provider_name == "whisperx"

    def test_routing_policy_cloud_first(self, mock_settings):
        """Test CLOUD_FIRST policy prefers cloud providers."""
        mock_settings.TRANSCRIPTION_ROUTING_POLICY = "cloud_first"
        
        with patch("app.services.capability_registry.WhisperXProvider") as mock_whisperx, \
             patch("app.services.capability_registry.DeepgramProvider") as mock_deepgram, \
             patch("app.services.capability_registry.GroqProvider") as mock_groq, \
             patch("app.services.capability_registry.OpenAIProvider") as mock_openai:
            
            mock_whisperx_instance = Mock()
            mock_whisperx_instance.provider_name = "whisperx"
            mock_whisperx_instance.model_id = "large-v3"
            mock_whisperx_instance.supports_diarization = True
            mock_whisperx_instance.supports_word_alignments = True
            mock_whisperx_instance.supported_languages = {"en"}
            mock_whisperx.return_value = mock_whisperx_instance
            
            mock_deepgram_instance = Mock()
            mock_deepgram_instance.provider_name = "deepgram"
            mock_deepgram_instance.model_id = "nova-2"
            mock_deepgram_instance.supports_diarization = True
            mock_deepgram_instance.supports_word_alignments = True
            mock_deepgram_instance.supported_languages = {"en"}
            mock_deepgram.return_value = mock_deepgram_instance
            
            mock_groq_instance = Mock()
            mock_groq_instance.provider_name = "groq"
            mock_groq_instance.model_id = "whisper-large-v3"
            mock_groq_instance.supports_diarization = False
            mock_groq_instance.supports_word_alignments = False
            mock_groq_instance.supported_languages = {"en"}
            mock_groq.return_value = mock_groq_instance
            
            mock_openai_instance = Mock()
            mock_openai_instance.provider_name = "openai"
            mock_openai_instance.model_id = "whisper-1"
            mock_openai_instance.supports_diarization = False
            mock_openai_instance.supports_word_alignments = False
            mock_openai_instance.supported_languages = {"en"}
            mock_openai.return_value = mock_openai_instance
            
            registry = create_capability_registry(mock_settings)
            
            # With no special requirements, cloud_first should prefer cloud
            provider = registry.get_transcription_provider()
            assert provider.provider_name != "whisperx"

    def test_routing_policy_fastest(self, mock_settings):
        """Test FASTEST policy prefers lowest latency."""
        mock_settings.TRANSCRIPTION_ROUTING_POLICY = "fastest"
        
        with patch("app.services.capability_registry.WhisperXProvider") as mock_whisperx, \
             patch("app.services.capability_registry.DeepgramProvider") as mock_deepgram, \
             patch("app.services.capability_registry.GroqProvider") as mock_groq, \
             patch("app.services.capability_registry.OpenAIProvider") as mock_openai:
            
            providers = ["whisperx", "deepgram", "groq", "openai"]
            for provider_name, mock in zip(providers, [mock_whisperx, mock_deepgram, mock_groq, mock_openai]):
                instance = Mock()
                instance.provider_name = provider_name
                instance.model_id = "test"
                instance.supports_diarization = True
                instance.supports_word_alignments = True
                instance.supported_languages = {"en"}
                mock.return_value = instance
            
            registry = create_capability_registry(mock_settings)
            
            # Groq has lowest estimated latency (5000ms/min)
            provider = registry.get_transcription_provider()
            assert provider.provider_name == "groq"

    def test_routing_policy_highest_quality(self, mock_settings):
        """Test HIGHEST_QUALITY policy prefers highest quality score."""
        mock_settings.TRANSCRIPTION_ROUTING_POLICY = "highest_quality"
        
        with patch("app.services.capability_registry.WhisperXProvider") as mock_whisperx, \
             patch("app.services.capability_registry.DeepgramProvider") as mock_deepgram, \
             patch("app.services.capability_registry.GroqProvider") as mock_groq, \
             patch("app.services.capability_registry.OpenAIProvider") as mock_openai:
            
            providers = ["whisperx", "deepgram", "groq", "openai"]
            for provider_name, mock in zip(providers, [mock_whisperx, mock_deepgram, mock_groq, mock_openai]):
                instance = Mock()
                instance.provider_name = provider_name
                instance.model_id = "test"
                instance.supports_diarization = True
                instance.supports_word_alignments = True
                instance.supported_languages = {"en"}
                mock.return_value = instance
            
            registry = create_capability_registry(mock_settings)
            
            # Deepgram has highest quality score (0.95)
            provider = registry.get_transcription_provider()
            assert provider.provider_name == "deepgram"

    def test_routing_policy_cost_optimized(self, mock_settings):
        """Test COST_OPTIMIZED policy prefers lowest cost."""
        mock_settings.TRANSCRIPTION_ROUTING_POLICY = "cost_optimized"
        
        with patch("app.services.capability_registry.WhisperXProvider") as mock_whisperx, \
             patch("app.services.capability_registry.DeepgramProvider") as mock_deepgram, \
             patch("app.services.capability_registry.GroqProvider") as mock_groq, \
             patch("app.services.capability_registry.OpenAIProvider") as mock_openai:
            
            providers = ["whisperx", "deepgram", "groq", "openai"]
            for provider_name, mock in zip(providers, [mock_whisperx, mock_deepgram, mock_groq, mock_openai]):
                instance = Mock()
                instance.provider_name = provider_name
                instance.model_id = "test"
                instance.supports_diarization = True
                instance.supports_word_alignments = True
                instance.supported_languages = {"en"}
                mock.return_value = instance
            
            registry = create_capability_registry(mock_settings)
            
            # WhisperX has 0 cost
            provider = registry.get_transcription_provider()
            assert provider.provider_name == "whisperx"

    def test_get_capability(self, registry):
        """Test getting capability for specific provider."""
        cap = registry.get_capability("deepgram")
        assert cap is not None
        assert cap.provider_name == "deepgram"
        assert cap.model_id == "nova-2"

    def test_get_capability_nonexistent(self, registry):
        """Test getting capability for nonexistent provider returns None."""
        cap = registry.get_capability("nonexistent")
        assert cap is None


class TestCreateCapabilityRegistry:
    """Test create_capability_registry factory function."""

    @pytest.fixture
    def mock_settings(self):
        """Mock settings object."""
        settings = Mock()
        settings.TRANSCRIPTION_ROUTING_POLICY = "local_first"
        settings.WHISPERX_MODEL = "large-v3"
        settings.WHISPERX_DEVICE = "cpu"
        settings.DEEPGRAM_API_KEY = "test_deepgram_key"
        settings.DEEPGRAM_MODEL = "nova-2"
        settings.GROQ_API_KEY = "test_groq_key"
        settings.GROQ_MODEL = "whisper-large-v3"
        settings.OPENAI_API_KEY = "test_openai_key"
        settings.OPENAI_WHISPER_MODEL = "whisper-1"
        settings.NVIDIA_NIM_BASE_URL = None
        settings.NVIDIA_NIM_MODEL = "parakeet-rnnt-1.1b"
        settings.NVIDIA_NIM_API_KEY = None
        return settings

    def test_create_from_settings(self, mock_settings):
        """Test factory creates registry from settings."""
        with patch("app.services.capability_registry.CapabilityRegistry") as mock_registry_class:
            mock_registry = Mock()
            mock_registry_class.return_value = mock_registry
            
            registry = create_capability_registry(mock_settings)
            
            mock_registry_class.assert_called_once()
            call_kwargs = mock_registry_class.call_args.kwargs
            assert call_kwargs["policy"] == "local_first"
            assert call_kwargs["whisperx_model"] == "large-v3"
            assert call_kwargs["deepgram_api_key"] == "test_deepgram_key"
            assert call_kwargs["groq_api_key"] == "test_groq_key"
            assert call_kwargs["openai_api_key"] == "test_openai_key"
            assert call_kwargs["nvidia_nim_base_url"] is None