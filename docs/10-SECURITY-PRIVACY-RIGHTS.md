# Security, Privacy, Content Rights and Platform Compliance

**Status:** PROPOSED

## 1. Security boundaries

- Workspace/resource authorization on every API operation.
- Secrets stored in a secret manager or encrypted at rest.
- Redact authorization headers, signed URLs and provider secrets from logs.
- Validate upload MIME/format using actual probing, not only filename.
- Malware scanning/quarantine strategy for untrusted uploaded files.
- URL ingestion must defend against SSRF and redirect/DNS rebinding.
- Isolate FFmpeg and other media tools with restricted filesystem/network privileges, resource limits and safe argument construction.
- Validate file paths and prevent traversal.
- Use CSRF/state protection for OAuth callbacks.
- Rate limit expensive endpoints.

## 2. AI safety and validation

- Treat transcripts, model responses, metadata and imported descriptions as untrusted data.
- Do not allow prompt injection from video speech to change system policy, secrets or tools.
- No model-generated shell commands, raw FFmpeg commands or arbitrary Python execution.
- AI edits must be allow-listed typed operations.
- Validate all generated timestamps and ensure they map to source evidence.
- Keep audit record of automatic approval decisions and the policy version.

## 3. Rights and consent

Before ingestion/publishing, capture user's rights basis: created/owned, licensed, client-authorized, public-domain, or other documented permission. The declaration is a workflow safeguard, not legal proof. Store source attribution, licence restrictions and any no-derivative/no-commercial conditions. Provide takedown/deletion workflow.

Do not assume a public URL or platform's public visibility grants download, derivative-work or commercial-use permission. Do not bypass DRM, login walls, private streams or access controls.

## 4. Third-party media

For B-roll, music, fonts, templates, sound effects and stock imagery:
- Store asset provider, original URL, licence type, attribution requirements, download date and checksum.
- Filter commercial-use and redistribution rights based on workspace use.
- Do not assume a free stock asset has unrestricted rights.
- Fail softly only by omitting optional asset; never silently use unlicensed material.

## 5. Privacy

- Define retention periods by asset/data class.
- Minimize stored face/voice embeddings and avoid identity recognition unless explicitly required and legally reviewed.
- Provide account disconnect and data deletion flows.
- Restrict transcript/recording access by workspace.
- Ensure model-provider data handling is disclosed/configurable.

## 6. Publishing permissions

Use official APIs and OAuth only. Verify app review, account type, page/channel roles, permissions, region and quotas. Do not automate platform UI or collect user passwords.

## 7. Operational security

Backups encrypted and tested. Dependencies scanned. Containers non-root where possible. Separate dev/test/prod credentials. Audit administrative operations. Establish incident and credential-rotation procedure.
