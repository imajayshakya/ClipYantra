"""ING-003 Capability registry for transcription provider selection."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set

from app.services.transcription_provider import (
    TranscriptionProvider,
    TranscriptionRequest,
    DeepgramProvider,
    GroqProvider,
    OpenAIProvider,
    NvidiaNimProvider,
    WhisperXProvider,
)


class RoutingPolicy(str, Enum):
    """Provider routing policies."""
    LOCAL_FIRST = "local_first"       # Prefer local (WhisperX), fallback to cloud
    CLOUD_FIRST = "cloud_first"       # Prefer cloud, fallback to local
    FASTEST = "fastest"               # Prefer fastest provider
    HIGHEST_QUALITY = "highest_quality"  # Prefer highest quality
    COST_OPTIMIZED = "cost_optimized"  # Prefer cheapest


@dataclass(frozen=True)
class ProviderCapability:
    """Provider capability description."""
    provider_name: str
    model_id: str
    supports_diarization: bool
    supports_word_alignments: bool
    supported_languages: Set[str]
    estimated_latency_ms_per_minute: int  # Estimated processing time
    cost_per_minute_usd: float  # Estimated cost (0 for local)
    quality_score: float  # 0-1 quality estimate


class CapabilityRegistry:
    """Registry for transcription provider selection."""

    def __init__(
        self,
        policy: RoutingPolicy = RoutingPolicy.LOCAL_FIRST,
        whisperx_model: str = "large-v3",
        whisperx_device: str = "auto",
        deepgram_api_key: Optional[str] = None,
        deepgram_model: str = "nova-2",
        groq_api_key: Optional[str] = None,
        groq_model: str = "whisper-large-v3",
        openai_api_key: Optional[str] = None,
        openai_model: str = "whisper-1",
        nvidia_nim_base_url: Optional[str] = None,
        nvidia_nim_model: str = "parakeet-rnnt-1.1b",
        nvidia_nim_api_key: Optional[str] = None,
    ):
        self._policy = policy
        self._providers: Dict[str, TranscriptionProvider] = {}
        self._capabilities: Dict[str, ProviderCapability] = {}

        # Initialize providers
        self._init_providers(
            whisperx_model=whisperx_model,
            whisperx_device=whisperx_device,
            deepgram_api_key=deepgram_api_key,
            deepgram_model=deepgram_model,
            groq_api_key=groq_api_key,
            groq_model=groq_model,
            openai_api_key=openai_api_key,
            openai_model=openai_model,
            nvidia_nim_base_url=nvidia_nim_base_url,
            nvidia_nim_model=nvidia_nim_model,
            nvidia_nim_api_key=nvidia_nim_api_key,
        )

    def _init_providers(
        self,
        whisperx_model: str,
        whisperx_device: str,
        deepgram_api_key: Optional[str],
        deepgram_model: str,
        groq_api_key: Optional[str],
        groq_model: str,
        openai_api_key: Optional[str],
        openai_model: str,
        nvidia_nim_base_url: Optional[str],
        nvidia_nim_model: str,
        nvidia_nim_api_key: Optional[str],
    ) -> None:
        """Initialize all available providers."""

        # WhisperX (local)
        try:
            provider = WhisperXProvider(
                model=whisperx_model,
                device=whisperx_device,
            )
            self._providers[provider.provider_name] = provider
            self._capabilities[provider.provider_name] = ProviderCapability(
                provider_name=provider.provider_name,
                model_id=provider.model_id,
                supports_diarization=provider.supports_diarization,
                supports_word_alignments=provider.supports_word_alignments,
                supported_languages=provider.supported_languages,
                estimated_latency_ms_per_minute=60_000 if whisperx_device != "cpu" else 120_000,
                cost_per_minute_usd=0.0,
                quality_score=0.9,
            )
        except Exception:
            pass  # WhisperX not available

        # Deepgram
        if deepgram_api_key:
            provider = DeepgramProvider(
                api_key=deepgram_api_key,
                model=deepgram_model,
            )
            self._providers[provider.provider_name] = provider
            self._capabilities[provider.provider_name] = ProviderCapability(
                provider_name=provider.provider_name,
                model_id=provider.model_id,
                supports_diarization=provider.supports_diarization,
                supports_word_alignments=provider.supports_word_alignments,
                supported_languages=provider.supported_languages,
                estimated_latency_ms_per_minute=10_000,
                cost_per_minute_usd=0.0043,  # Nova-2 pricing
                quality_score=0.95,
            )

        # Groq
        if groq_api_key:
            provider = GroqProvider(
                api_key=groq_api_key,
                model=groq_model,
            )
            self._providers[provider.provider_name] = provider
            self._capabilities[provider.provider_name] = ProviderCapability(
                provider_name=provider.provider_name,
                model_id=provider.model_id,
                supports_diarization=provider.supports_diarization,
                supports_word_alignments=provider.supports_word_alignments,
                supported_languages=provider.supported_languages,
                estimated_latency_ms_per_minute=5_000,
                cost_per_minute_usd=0.0001,  # Very cheap
                quality_score=0.9,
            )

        # OpenAI
        if openai_api_key:
            provider = OpenAIProvider(
                api_key=openai_api_key,
                model=openai_model,
            )
            self._providers[provider.provider_name] = provider
            self._capabilities[provider.provider_name] = ProviderCapability(
                provider_name=provider.provider_name,
                model_id=provider.model_id,
                supports_diarization=provider.supports_diarization,
                supports_word_alignments=provider.supports_word_alignments,
                supported_languages=provider.supported_languages,
                estimated_latency_ms_per_minute=15_000,
                cost_per_minute_usd=0.006,  # Whisper pricing
                quality_score=0.92,
            )

        # NVIDIA NIM
        if nvidia_nim_base_url:
            provider = NvidiaNimProvider(
                base_url=nvidia_nim_base_url,
                model=nvidia_nim_model,
                api_key=nvidia_nim_api_key,
            )
            self._providers[provider.provider_name] = provider
            self._capabilities[provider.provider_name] = ProviderCapability(
                provider_name=provider.provider_name,
                model_id=provider.model_id,
                supports_diarization=provider.supports_diarization,
                supports_word_alignments=provider.supports_word_alignments,
                supported_languages=provider.supported_languages,
                estimated_latency_ms_per_minute=8_000,
                cost_per_minute_usd=0.0,  # Self-hosted
                quality_score=0.93,
            )

    def get_provider(self, name: str) -> Optional[TranscriptionProvider]:
        """Get provider by name."""
        return self._providers.get(name)

    def get_transcription_provider(
        self,
        hint: Optional[str] = None,
        language: Optional[str] = None,
        diarization: bool = False,
        word_alignments: bool = False,
    ) -> TranscriptionProvider:
        """
        Select best provider based on policy and requirements.
        
        Args:
            hint: Explicit provider hint (e.g., "whisperx", "deepgram")
            language: Target language code
            diarization: Whether diarization is required
            word_alignments: Whether word alignments are required
            
        Returns:
            Selected transcription provider
            
        Raises:
            ValueError: If no suitable provider found
        """
        # If explicit hint provided, use it if available
        if hint:
            provider = self._providers.get(hint)
            if provider is None:
                raise ValueError(f"Provider '{hint}' not available")
            
            # Validate capabilities
            if diarization and not provider.supports_diarization:
                raise ValueError(f"Provider '{hint}' does not support diarization")
            if word_alignments and not provider.supports_word_alignments:
                raise ValueError(f"Provider '{hint}' does not support word alignments")
            if language and language not in provider.supported_languages:
                raise ValueError(f"Provider '{hint}' does not support language: {language}")
            
            return provider

        # Filter providers by requirements
        candidates = []
        for name, provider in self._providers.items():
            cap = self._capabilities[name]
            
            if diarization and not cap.supports_diarization:
                continue
            if word_alignments and not cap.supports_word_alignments:
                continue
            if language and language not in cap.supported_languages:
                continue
            
            candidates.append((name, cap))

        if not candidates:
            raise ValueError(
                f"No provider available for requirements: "
                f"language={language}, diarization={diarization}, "
                f"word_alignments={word_alignments}"
            )

        # Sort by policy
        if self._policy == RoutingPolicy.LOCAL_FIRST:
            # Prefer local (whisperx), then cloud
            candidates.sort(key=lambda x: (0 if x[0] == "whisperx" else 1, x[1].estimated_latency_ms_per_minute))
        elif self._policy == RoutingPolicy.CLOUD_FIRST:
            # Prefer cloud, then local
            candidates.sort(key=lambda x: (0 if x[0] != "whisperx" else 1, x[1].estimated_latency_ms_per_minute))
        elif self._policy == RoutingPolicy.FASTEST:
            candidates.sort(key=lambda x: x[1].estimated_latency_ms_per_minute)
        elif self._policy == RoutingPolicy.HIGHEST_QUALITY:
            candidates.sort(key=lambda x: -x[1].quality_score)
        elif self._policy == RoutingPolicy.COST_OPTIMIZED:
            candidates.sort(key=lambda x: x[1].cost_per_minute_usd)

        best_name = candidates[0][0]
        return self._providers[best_name]

    def list_providers(self) -> List[ProviderCapability]:
        """List all available provider capabilities."""
        return list(self._capabilities.values())

    def get_capability(self, name: str) -> Optional[ProviderCapability]:
        """Get capability for a specific provider."""
        return self._capabilities.get(name)

    @property
    def policy(self) -> RoutingPolicy:
        return self._policy


def create_capability_registry(config) -> CapabilityRegistry:
    """Create capability registry from config."""
    return CapabilityRegistry(
        policy=RoutingPolicy(config.TRANSCRIPTION_ROUTING_POLICY),
        whisperx_model=config.WHISPERX_MODEL,
        whisperx_device=config.WHISPERX_DEVICE,
        deepgram_api_key=getattr(config, "DEEPGRAM_API_KEY", None),
        deepgram_model=getattr(config, "DEEPGRAM_MODEL", "nova-2"),
        groq_api_key=getattr(config, "GROQ_API_KEY", None),
        groq_model=getattr(config, "GROQ_MODEL", "whisper-large-v3"),
        openai_api_key=getattr(config, "OPENAI_API_KEY", None),
        openai_model=getattr(config, "OPENAI_WHISPER_MODEL", "whisper-1"),
        nvidia_nim_base_url=getattr(config, "NVIDIA_NIM_BASE_URL", None),
        nvidia_nim_model=getattr(config, "NVIDIA_NIM_MODEL", "parakeet-rnnt-1.1b"),
        nvidia_nim_api_key=getattr(config, "NVIDIA_NIM_API_KEY", None),
    )