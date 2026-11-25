---
name: visual-qa
description: 'Use after implementing or changing ClipYantra UI to capture screenshots, compare against approved designs, check responsive layout, component states, visual regressions and real interactions.'
argument-hint: '[route, viewport or UI slice]'
---

# Visual QA

1. Identify approved screen spec and target viewport set.
2. Use deterministic fixture data and representative media samples.
3. Capture screenshots at required sizes.
4. Compare hierarchy, spacing, typography, tokens, alignment, clipping and component states to approved design.
5. Exercise primary and secondary controls; do not accept static-looking but inert UI.
6. Check empty/loading/error/success/disabled states.
7. Check responsive overflow and Clip Studio timeline behavior.
8. Run accessibility automation and manual keyboard checks where available.
9. Report screenshot paths, browser/version, viewport, exact tests and deviations.
10. Do not update visual baselines to hide unexplained regressions. Do not self-approve implementation.
