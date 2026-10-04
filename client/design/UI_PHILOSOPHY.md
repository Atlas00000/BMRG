# BMRG Client — UI Philosophy

**System name:** Ledger Noir + Signal Teal  
**Phase:** Foundations only (tokens → primitives → patterns → shells)  
**Status:** Locked for UI-W01 design foundation  
**Non-goal:** Section content layouts, feature redesign, marketing pages

---

## 1. North star

An **executive trading OS** console: dark ledger canvas, lifted planes, hairline structure, asymmetric composition. The UI must feel like a risk desk instrument — not a SaaS dashboard, not a crypto terminal, not an AI demo.

**Feel adjectives:** sober · precise · lifted · asymmetric · signal-led · calm urgency · tactile chrome · metric-first

**Obviousness bar:** old vs new must be unmistakable in **&lt;2 seconds** (canvas, type, chrome) before reading any section copy.

---

## 2. Kill list

| Kill | Why |
| --- | --- |
| Equal card grids as default layout | Bootstrap admin language |
| Purple / indigo AI gradients | Generic LLM UI slop |
| Neon green-on-black crypto glow | Entertainment, not ops |
| Clip art, emojis, stock illustrations | Cheap; breaks trust |
| Balance-as-hero vanity metrics | Violates edge-framework vocabulary |
| Mega single-file CSS / page-local themes | Non-modular; uninheritable |
| Motion for decoration | Distracts from state |
| “AI confidence” as a KPI label | Forbidden vocabulary |

---

## 3. Palette tokens (Ledger Noir + Signal Teal)

| Token | Role | Value |
| --- | --- | --- |
| `--ln-canvas` | App void | `#070A0C` |
| `--ln-canvas-glow` | Atmospheric wash (teal, very low) | radial teal @ 4–6% |
| `--ln-plane` | Lifted content | `#0E1419` |
| `--ln-plane-2` | Nested lift | `#141C24` |
| `--ln-hairline` | Structure | `rgba(232,238,242,0.08)` |
| `--ln-hairline-strong` | Active edge | `rgba(45,212,191,0.35)` |
| `--ln-ink` | Primary text | `#E8EEF2` |
| `--ln-ink-muted` | Secondary | `#8B9AAB` |
| `--ln-ink-faint` | Tertiary | `#5C6B7A` |
| `--ln-signal` | Accent / CTA / live | `#2DD4BF` |
| `--ln-signal-dim` | Accent wash | `rgba(45,212,191,0.12)` |
| `--ln-warn` | Soft fuse / fragile | `#E8A54B` |
| `--ln-halt` | Hard stop / L3 | `#E85D5D` |
| `--ln-ok` | Pass / fire allow path | `#5BC98A` |
| `--ln-skip` | Withhold / skip | `#6B8CAE` |

Accent is **signal only** — never paint large fills teal.

---

## 4. Typography

| Role | Family | Notes |
| --- | --- | --- |
| Display | **Fraunces** (soft optical, editorial) | Page titles, brand wordmark — sober, not playful |
| Body / UI | **IBM Plex Sans** | Ops density, high legibility |
| Metrics | **IBM Plex Sans** `font-variant-numeric: tabular-nums` | EF, E_N, WR, n |
| Mono / IDs | **IBM Plex Mono** | magic, semver, event_id |

Scale (rem @ 16px root): `display` 2.25 · `title` 1.375 · `body` 0.9375 · `label` 0.75 · `micro` 0.6875  
Tracking: display slightly tight; labels slightly wide (0.04em).

---

## 5. Motion grammar

| Primitive | Use | Duration |
| --- | --- | --- |
| `PageEnter` | Staged opacity + 8–12px Y on route mount | 280–420ms stagger |
| `NumberTick` | Metric value change | 320ms ease-out |
| `StateCrossfade` | Badge / mode / halt transitions | 180ms |
| Route continuity | Shared shell; content only remounts | — |

**Rules:** ease `cubic-bezier(0.22, 1, 0.36, 1)`; respect `prefers-reduced-motion: reduce` (instant opacity, no travel). Motion explains **state**, never entertains.

---

## 6. Layout grammar

- **Asymmetric shell:** narrow identity rail + wide stage (not equal columns of cards).
- **Hairline structure** over heavy borders/shadows.
- **One composition** on Home proof: brand/status strip + primary signal + next action — not a widget dashboard.
- Elevation: plane lift via surface tone + 1px hairline, not multi-layer drop shadows.

---

## 7. Modular file map

```
client/
  design/
    UI_PHILOSOPHY.md          ← this file
    tokens.css                ← CSS variables
    tokens.ts                 ← typed token names
    backendMap.ts             ← API enums → visual tone
    motion.css                ← keyframes + reduced-motion
  src/
    styles/global.css         ← canvas, reset, type imports
    components/
      primitives/             ← Surface, Text, Button, Input, Badge, Icon
      motion/                 ← PageEnter, NumberTick, StateCrossfade
      shells/                 ← AppShell, PageHeader, ActionRail
      patterns/               ← MetricStrip, EmptyState, Skeleton*
    routes/Home.tsx           ← foundation proof surface
```

Compose: **pages import shells + patterns; patterns import primitives; everyone consumes tokens.**

---

## 8. Backend ↔ UI mapping

| Backend concept | Source | UI token / component |
| --- | --- | --- |
| `zone` Fragile / Strong_* | health_vector | `Badge` tone `warn` / `signal` / `ok` |
| `lifecycle` Stable / Near frontier / … | AOS / W250 | `Badge` + `StateCrossfade` |
| `decision` FIRE / ALLOW_UNCERTAIN / SKIP | ledger | `ok` / `warn` / `skip` chips |
| `InpAiOsMode` OFF / SHADOW / LIVE_WITHHOLD | EA / preset | mode chip; signal only when LIVE_WITHHOLD |
| `halt` L3 / equity / daily | Risk / AOS | `halt` tone; **outranks** L2 skip visually |
| Gate ACCEPT / REJECT | prove scorecards | `ok` / `halt` strip edges |
| Magic / semver / preset_id | identity | Mono `Text` |

Frontend **hugs** backend enums — no invented “confidence” colours.

---

## 9. Empty / loading

- Skeletons that match MetricStrip / plane geometry
- Short operational copy (“No LATEST_EVAL artefact”)
- **Never** emoji, clip art, or illustration placeholders

---

## 10. Out of scope (this phase)

- Per-section content redesign (Health / Live / Layers / … layouts)
- Chart trading, order tickets, EDX reopen
- Full OpenAPI / artefact adapters (UI-W02+)
- FT console ship
- Visual regression CI pack (UI-W11)

Later workstreams inherit this system; they do not redefine tokens ad hoc.
