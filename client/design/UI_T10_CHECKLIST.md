# UI-T10 — Foundation acceptance checklist

## Obvious difference (&lt;2s)

- [x] Canvas is near-black with teal atmospheric wash (not flat Bootstrap gray/white)
- [x] Display type is Fraunces (not Inter/system)
- [x] Asymmetric rail + stage (not equal card dashboard)
- [x] Signal teal used only for accent / active / CTA
- [x] Hairline structure, lifted planes — no neon glow stacks

## Modular system

- [x] `design/tokens.css` + `design/tokens.ts` names match `UI_PHILOSOPHY.md`
- [x] Primitives / motion / shells / patterns in separate folders
- [x] `backendMap.ts` maps zone · lifecycle · decision · mode · verdict · halt
- [x] Home proves shell; other routes inherit chrome via placeholders

## A11y / motion

- [x] `:focus-visible` uses signal ring token
- [x] Badges / buttons have text labels (no emoji-only controls)
- [x] `prefers-reduced-motion` collapses PageEnter travel + skeleton animation
- [x] Empty states are copy-only

## Out of scope (confirmed not done)

- [x] No Health/Live/Layers section content redesign
- [x] No trade / order UI
- [x] No OpenAPI artefact adapters (UI-W02+)
