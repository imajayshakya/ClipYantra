# Brand and Visual Direction

**Status:** APPROVED v1 - Direction A is the primary implementation direction  
**Approval:** `APPROVE VISUAL DIRECTION v1`  
**Date:** 2026-11-22  
**Prerequisites:** `APPROVE UX v1`, `APPROVE IA v1`

## Product name

ClipYantra — working product name. Confirm trademark/domain availability separately before public launch.

## Brand personality

- Intelligent, but not magical or opaque.
- Capable and professional, not intimidating.
- Creative, but not playful to the point of reducing trust.
- Efficient and calm under heavy processing workloads.
- Technically sophisticated without exposing unnecessary complexity.

## Visual directions to explore

### Direction A — Calm Creator Workstation (recommended candidate)

**Core concept**: A focused, low-fatigue editing environment that recedes into the background so the creator's content takes center stage. Dark graphite surfaces reduce eye strain during long editing sessions; restrained indigo accents guide attention without screaming.

| Attribute | Specification |
|---|---|
| **Canvas** | `#0F1113` (near-black graphite) |
| **Surface / Panel** | `#181C1F` (elevated panel) |
| **Surface hover** | `#1E2327` |
| **Border / Divider** | `#2A2F34` |
| **Text primary** | `#E8EAED` |
| **Text secondary** | `#9AA3AC` |
| **Text muted** | `#6B737C` |
| **Brand accent (indigo)** | `#4F7CFF` — primary actions, focus rings, active navigation |
| **Brand accent hover** | `#3D6BFF` |
| **Success (teal)** | `#14B8A6` — completed jobs, published posts, valid states |
| **Warning (amber)** | `#F59E0B` — attention needed, queued, review required |
| **Error / Destructive (red)** | `#EF4444` — failed jobs, delete actions, validation errors |
| **Focus ring** | `0 0 0 2px #4F7CFF` |
| **Typography** | UI: `Inter` / system sans; Mono: `JetBrains Mono` / `SF Mono` / `Consolas` for timecodes, durations, code |
| **Type scale** | Display: 28/36; H1: 24/32; H2: 20/28; H3: 16/24; Body: 14/22; Small: 12/18; Micro: 11/16 |
| **Tabular numerals** | Enabled for all timecodes, durations, metrics, costs |
| **Spacing base** | 4px (0.25rem) |
| **Density tiers** | Management: spacious (16px base); Clip Studio: dense (8px base); Monitoring: compact (6px base) |
| **Radius** | 4px (controls), 8px (panels), 12px (modals), 9999px (pills) |
| **Elevation** | 0: none; 1: `0 1px 2px rgba(0,0,0,0.3)`; 2: `0 4px 8px rgba(0,0,0,0.4)`; 3: `0 8px 24px rgba(0,0,0,0.5)` |
| **Motion** | 120ms ease-out for micro-interactions; 200ms for panel transitions; respect `prefers-reduced-motion` |
| **Icon family** | Phosphor Icons (duotone weight for active, regular for inactive) or Lucide |
| **Logo mark** | Abstract frame/crop with subtle play-head motion cue; works monochrome at 16px |

#### Screen applications — Direction A

| Screen | Layout & Behavior |
|---|---|
| **1. Overview Dashboard** | Left rail (64px collapsed, 240px expanded) with brand mark + 7 primary nav items. Top bar: workspace switcher, search (Cmd+K), notifications, user menu. Main grid: 12-col responsive. Hero metric row (4 cards: processing, ready to review, scheduled, published this week) — teal/amber/indigo status dots. Below: recent activity feed (virtual list, 20 items), quick actions (New Import, Clip Studio shortcuts). Density: spacious. Empty state: centered illustration + "Import your first video" CTA (indigo primary). |
| **2. Video Library / List** | Toolbar: search, filter chips (profile, status, date range), view toggle (grid/list), sort. List density: 56px row height; hover reveals actions (Open Studio, Duplicate, Delete). Grid view: 16:9 thumb (160×90) + title + meta badges (profile, duration, candidate count). Status pill: teal=complete, amber=processing, indigo=queued, red=failed, gray=draft. Keyboard: `j/k` navigate, `Enter` open, `/` focus search. Infinite scroll (50/page). |
| **3. Clip Studio (Preview + Timeline + Inspector)** | Three-zone layout: **Left (280px)** — Candidate list / Transcript / Assets tabs. **Center (flex-1)** — Video preview (16:9, letterboxed) with transport controls (space=play/pause, ←/→=frame, Shift+←/→=5s). **Right (320px)** — Contextual inspector: Timeline (tracks: Video, Audio, Captions, B-roll, Effects), Properties panel (crop, transform, caption style, effects). Timeline: dark surface `#0F1113`, track height 48px default / 32px compact, playhead `#4F7CFF`, selection teal. Zoom: `Ctrl+=/-`, wheel. Undo/redo: `Ctrl+Z/Y` toast confirmation. Density: dense (8px base). Focus trap in inspector when open. |
| **4. Publishing Calendar** | Monthly grid default; Week/Day/Views toggle. Each day cell: min-height 100px, max 3 event chips before `+N more`. Chip: platform icon + title truncate + time + status dot. Drag-drop reschedule (indigo drag preview). Right sidebar (320px): scheduled post detail — metadata, platform preview, approve/reject actions. Keyboard: `←/→` day, `↑/↓` event, `Enter` open, `n` new. Density: spacious. |
| **5. AI Provider Settings** | Two-panel: left provider list (cards: logo, name, status badge, models count, cost tier), right detail drawer (380px). Detail: capability matrix (table: modality ✓/✗, languages, max tokens, latency tier, cost/1k), routing rules (profile→provider priority drag list), cost limits (per-job, daily, monthly), credentials (masked, test connection button). Status badges: teal=healthy, amber=degraded, red=error, gray=disabled. Density: spacious. |

---

### Direction B — Editorial Light Studio

**Core concept**: A calm, paper-like workspace that feels like a well-designed editorial tool. Warm off-white surfaces, deep ink typography, generous whitespace. The deep violet/blue accent provides brand presence without overwhelming content. Excellent for library, planning, analytics — the editor preview must prove contrast adequacy.

| Attribute | Specification |
|---|---|
| **Canvas** | `#FAF9F6` (warm off-white) |
| **Surface / Panel** | `#FFFFFF` (pure white panels) |
| **Surface hover** | `#F5F3EF` |
| **Border / Divider** | `#E5E2DB` |
| **Text primary** | `#1A1A2E` (deep ink) |
| **Text secondary** | `#5A5A7A` |
| **Text muted** | `#9A9AA8` |
| **Brand accent (deep violet-blue)** | `#4C3FD6` — primary actions, focus rings, active navigation |
| **Brand accent hover** | `#3D30C8` |
| **Success (emerald)** | `#059669` — completed, published, valid |
| **Warning (amber)** | `#D97706` — attention, queued, review |
| **Error / Destructive (red)** | `#DC2626` — failed, delete, validation |
| **Focus ring** | `0 0 0 2px #4C3FD6` |
| **Typography** | UI: `Fraunces` (display) + `Inter` (UI) or `DM Sans`; Mono: `JetBrains Mono` / `SF Mono` for timecodes |
| **Type scale** | Display: 32/40; H1: 28/36; H2: 22/30; H3: 18/26; Body: 15/24; Small: 13/20; Micro: 12/18 |
| **Tabular numerals** | Enabled for all timecodes, durations, metrics, costs |
| **Spacing base** | 4px (0.25rem) |
| **Density tiers** | Management: generous (20px base); Clip Studio: balanced (12px base); Monitoring: comfortable (14px base) |
| **Radius** | 6px (controls), 10px (panels), 14px (modals), 9999px (pills) |
| **Elevation** | 0: none; 1: `0 1px 3px rgba(0,0,0,0.08)`; 2: `0 4px 12px rgba(0,0,0,0.12)`; 3: `0 8px 28px rgba(0,0,0,0.16)` |
| **Motion** | 150ms ease-out for micro-interactions; 250ms for panel transitions; respect `prefers-reduced-motion` |
| **Icon family** | Phosphor Icons (fill weight for active, regular for inactive) or Heroicons outline |
| **Logo mark** | Same abstract frame/crop concept; deep violet mark on warm white; monochrome ink variant |

#### Screen applications — Direction B

| Screen | Layout & Behavior |
|---|---|
| **1. Overview Dashboard** | Left rail (72px collapsed, 260px expanded) with wordmark + 7 nav items (icon + label). Top bar: workspace, search, notifications, profile — lower contrast, subtle shadow. Main: 12-col, generous gutters (24px). Hero metrics: 4 large cards with subtle icon illustrations, typographic emphasis (Fraunces display numbers). Activity feed: card-based, softer shadows. Empty state: editorial illustration + "Begin with your first import" (violet primary). Density: generous. |
| **2. Video Library / List** | Toolbar: search (prominent), filter drawer (slides from right), view toggle, sort. List: 64px row, generous padding. Grid: 16:9 thumb (192×108) with subtle drop shadow, title in Fraunces medium. Status: colored left border (4px) + text label — more editorial, less "pill". Hover: subtle lift (elevation 1). Keyboard same as Direction A. Density: generous. |
| **3. Clip Studio (Preview + Timeline + Inspector)** | **CRITICAL CHALLENGE**: Light preview surface must not wash out video content. Solution: Preview zone uses `#1A1A2E` (ink) background with subtle vignette; transport controls float on preview with white icons. Left zone (300px): tabs with ink background, white text. Center: preview dominates. Right zone (340px): inspector on white surface, subtle divider. Timeline: ink background `#1A1A2E`, track height 52px, playhead violet `#4C3FD6`, selection emerald. Properties: generous form spacing, grouped sections. Density: balanced. Focus: visible violet ring on all interactive elements. |
| **4. Publishing Calendar** | Monthly grid, generous cell padding (16px). Day number in Fraunces. Event chips: rounded, violet/emerald/amber/red backgrounds with white text, platform icon. `+N more` link opens day drawer (right, 360px). Week/Day views: time-slot grid, drag-drop with violet drag preview. Sidebar: post detail with editorial typography, platform preview in phone frame. Density: generous. |
| **5. AI Provider Settings** | Left: provider cards on white, subtle border, violet accent top border (3px) for active. Right drawer (400px): capability matrix on alternating row stripes (`#FAF9F6` / `#FFFFFF`), routing rules as reorderable cards, cost limits in grouped fieldsets. Credentials: masked, "Test" button violet outline. Density: generous. |

---

### Direction C — Broadcast Control Room (Conditional)

**Core concept**: High-density, dark, status-rich interface for live monitoring and multi-stream operations. Pronounced status colors, persistent activity rail, compact information design. Only for dedicated live-operations mode if user research validates Persona 3 (gaming/streamer) + Persona 5 (operator) workflows.

| Attribute | Specification |
|---|---|
| **Canvas** | `#0A0E12` |
| **Surface** | `#11161B` |
| **Border** | `#1E2630` |
| **Text primary** | `#E0E4EA` |
| **Text secondary** | `#8B95A1` |
| **Brand accent (cyan)** | `#00D4FF` |
| **Status colors** | Live=red `#FF3B30`, Recording=red pulse, Queued=amber `#FFCC00`, Processing=cyan `#00D4FF`, Complete=green `#34C759`, Error=red `#FF453A` |
| **Typography** | UI: `IBM Plex Sans` + `IBM Plex Mono`; tight leading |
| **Density** | Compact (6px base) across all screens |
| **Motion** | Minimal; status pulses, real-time updates |
| **Use case** | Live ingest monitor, multi-source switching, real-time clipping — NOT for general Clip Studio editing |

---

## Side-by-side comparison: Dashboard & Clip Studio

| Aspect | Direction A (Calm Workstation) | Direction B (Editorial Light) |
|---|---|---|
| **Dashboard feel** | Technical, tool-like, focus on data density | Editorial, magazine-like, focus on readability |
| **Clip Studio preview** | Dark surround — video pops naturally | Light surround — requires ink preview zone |
| **Timeline contrast** | Native dark — excellent for waveforms | Ink background — must verify waveform visibility |
| **Long-session comfort** | High (dark reduces eye strain) | Medium (light can cause fatigue) |
| **Brand presence** | Restrained indigo — professional | Violet accent — more distinctive |
| **Accessibility risk** | Low (dark mode native) | **Medium** — must verify 4.5:1 on all surfaces, especially preview overlay controls |
| **Implementation complexity** | Standard dark theme | Light theme + dark preview zone = dual-surface |

---

## Logo concept prompts (for designer exploration)

1. **Frame + Playhead**: Abstract rectangular frame (9:16 proportion) with a thin vertical line (playhead) offset from center suggesting motion. Works at 16px as monochrome glyph.
2. **Connected Nodes**: Three circular nodes connected by bezier curves suggesting timeline segments; one node highlighted. Scales to favicon.
3. **Crop Mark + Arrow**: Minimal crop marks at corners with a subtle forward arrow integrating into the right mark. Suggests "create clip from source".
4. **Wordmark integration**: "ClipYantra" in Fraunces/Inter with custom ligature on "Clip" — the "C" and "l" subtly form a frame shape.

**Anti-patterns to avoid**: Literal scissors ✂️, magic wand ✨, generic play ▶, complex gradients, thin lines that vanish at small sizes.

**Required formats**: Monochrome app icon (1024→16px), favicon (32px), horizontal wordmark (light/dark), export watermark (semi-transparent, 12% opacity).

---

## Accessibility requirements (both directions)

| Requirement | Direction A | Direction B |
|---|---|---|
| **Color contrast (text)** | 4.5:1 minimum on all surfaces | 4.5:1 minimum; verify on warm white + ink |
| **Color contrast (UI controls)** | 3:1 minimum on borders, focus rings | 3:1 minimum; verify violet on white |
| **Focus indicators** | 2px indigo ring, visible on dark | 2px violet ring, visible on light |
| **Status not color-only** | Icon + text label + color | Icon + text label + colored border |
| **Reduced motion** | All transitions respect `prefers-reduced-motion` | All transitions respect `prefers-reduced-motion` |
| **Zoom / Reflow** | 200% zoom, no horizontal scroll | 200% zoom, no horizontal scroll |
| **Tabular numerals** | Required for timecodes, metrics | Required for timecodes, metrics |

---

## Trade-offs summary

| Dimension | Direction A | Direction B |
|---|---|---|
| **Creator editing comfort (long sessions)** | ✅ Excellent — dark native | ⚠️ Good — light may fatigue |
| **Library/Analytics readability** | ✅ Good — spacious tables | ✅ Excellent — editorial typography |
| **Brand distinctiveness** | ⚠️ Professional but conventional | ✅ Stronger editorial personality |
| **Implementation effort** | ✅ Single dark theme | ⚠️ Dual-surface (light UI + dark preview) |
| **Accessibility baseline** | ✅ Easier (dark mode native) | ⚠️ Requires careful contrast audit |
| **Video preview fidelity** | ✅ Natural (dark surround) | ⚠️ Needs ink preview zone design |
| **Print/export friendliness** | ⚠️ Dark backgrounds | ✅ Light surfaces print naturally |

---

## Recommendation

**Proceed with Direction A (Calm Creator Workstation) as the primary design exploration**, with Direction B (Editorial Light Studio) developed in parallel for the Dashboard, Library, Calendar, and Settings screens to validate the editorial aesthetic. Direction A's dark-native approach aligns with:
- Clip Studio's preview/timeline requirements (video content pops on dark)
- Long editing sessions (reduced eye strain per UX research pain points)
- Accessibility baseline (simpler contrast compliance)
- Technical/professional brand personality

**Direction B** should be fully designed for Dashboard, Library, Calendar, Settings to evaluate whether the editorial personality justifies the dual-surface complexity for Clip Studio.

**Direction C** is deferred — only if live-monitoring workflows are validated (OUT-004) and user research confirms need.

---

## Approved next step

1. Direction A — Calm Creator Workstation is the primary wireframe and implementation direction.
2. Complete low-fidelity wireframes and request `APPROVE WIREFRAMES v1`.
3. After wireframe approval, produce the semantic design system and interaction/responsive specifications.
4. Record any later Direction B or C adoption through an explicit design change request.

---

## Gate status

**Current:** APPROVED v1 - **`APPROVE VISUAL DIRECTION v1`** received.

Direction A — Calm Creator Workstation is the primary visual direction for wireframes and implementation. Direction B remains a reference for management-screen comparison and may be changed only through a design change request.
