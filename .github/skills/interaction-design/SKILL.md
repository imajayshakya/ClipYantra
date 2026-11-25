---
name: interaction-design
description: 'Use when specifying ClipYantra user interactions, editor gestures, undo/redo, autosave, dialogs, keyboard shortcuts, feedback, motion, transitions and error recovery.'
argument-hint: '[interaction or workflow]'
---

# Interaction Design

1. Define trigger, system response, feedback, resulting state and recovery path for every meaningful action.
2. Make loading/progress truthful; do not invent percentages.
3. Specify keyboard and pointer/touch interaction.
4. For Clip Studio, provide non-drag alternatives for trim, split, move and timing edits.
5. Treat editing as reversible, versioned operations; generated sources remain immutable.
6. AI edits return typed allow-listed operations, preview a diff and require user acceptance before apply.
7. Autosave communicates saving/saved/failure/conflict.
8. Destructive actions explain consequences and support undo where possible.
9. Motion must clarify cause/effect and respect reduced-motion settings.
10. Document state transitions and edge cases, not just the happy path.
