---
name: provider-capability-routing
description: Designs model registry, capability checks, routing profiles and provider fallback safely.
---

# Provider Capability Routing

Read `docs/05-AI-PROVIDER-STRATEGY.md`. Separate provider transport from model capabilities. Validate input modalities, output schema, languages, file duration/size, context, local runtime, pricing and quotas. Provide local-first, balanced, cloud-first and manual modes. Never silently route to a cloud service when the user requested local-only.
