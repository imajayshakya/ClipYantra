# Licensing and Third-Party Use

**Status:** REVIEW REQUIRED — not legal advice

## 1. SupoClip licence boundary

The SupoClip README and root `LICENSE` identify the repository as AGPL-3.0. The reviewed app-guide self-host section also contains a different phrase, “SupoClip Noncommercial Source License”. This is a documentation/licence inconsistency that must be resolved against the exact commit/tag and copyright holder before source reuse.

ClipYantra's default approach is **feature-level inspiration only**:
- Independently design equivalent workflow patterns.
- Do not copy source files, code blocks, prompts, UI assets, templates, fonts or substantial text.
- Keep a record of repository review and independent implementation decisions.
- If any code is proposed for reuse, stop and request licence/legal review first.

AGPL can impose source-availability obligations on modified network-served versions and redistribution. The exact obligations depend on the facts and implementation. Obtain qualified legal advice before incorporating AGPL code into a proprietary/commercial product.

## 2. Dependency approval checklist

For every new library/model/asset:
- Name, version, upstream URL and maintainer.
- Licence and whether commercial use/modification/redistribution is permitted.
- Transitive dependency licence scan.
- Security history and maintenance status.
- Data/model licence and acceptable use.
- Attribution or notice requirements.
- Whether dependencies are bundled or called as external services.
- Approval recorded in `docs/engineering/DECISIONS.md`.

## 3. Media asset licences

Track licence/source for stock footage, music, fonts, sound effects, transitions, icons and templates. An asset being free to download is not proof of commercial-use rights. Keep attribution and restrictions with the asset.

## 4. Model/API terms

At implementation time, review provider terms for commercial use, data retention, training use, regional availability, rate limits, model licence and output terms. Hosted API access and downloadable model weights may have different terms.

## 5. Records

Maintain `THIRD_PARTY_NOTICES.md` when the project begins adding dependencies/assets. No dependency is approved solely because it appears in a reference repository.
