---
name: provider-integration
description: Add or update one AI provider through the provider/capability registry.
agent: ai-provider-specialist
---

Integrate only the provider/model requested in an approved slice.

Verify official docs at implementation time: model ID, API shape, modalities, language, maximum file/input size, timestamps/diarization, rate limits, price, data handling and licence. Record documentation URL and verification date.

Implement adapter → normalized schema → capability metadata → timeout/retry policy → usage metrics → mocked tests → optional live smoke test only with explicitly configured credentials. Do not expose secrets or silently fall back to cloud when the user selected local-only. Do not assume NVIDIA API Catalog and NIM have identical interfaces.
