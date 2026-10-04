# App theme — palette options

**Purpose:** Aesthetic starting point for the BMRG client homepage, then other pages.  
**Scope:** Colour scheme / vibe first; functionality later.  
**Constraint:** Light + dark variants for every option. Avoid generic AI defaults (purple SaaS, cream/terracotta cliché, neon glow, candy pills).

---

## 1. Ledger Graphite + Verdigris

**Vibe:** Quiet institutional desk — matte metal, museum lighting, one cool accent.  
Best if you want “trading OS” without crypto-dashboard energy.

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#F3F1EC` | `#121416` |
| Ink | `#1A1D21` | `#E8E6E1` |
| Accent | `#2F6F68` | `#5FA89F` |
| Hairline | `#D5D2CB` | `#2A2E33` |
| Warn | `#A65D3B` | `#C9845F` |

---

## 2. Harbour Night + Fog Horn

**Vibe:** North-sea terminal at dusk — deep blue-black, mist grey, a single fog-light amber.  
More cinematic; still restrained if amber stays sparse.

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#EEF1F4` | `#0B1218` |
| Ink | `#15202B` | `#DCE4EC` |
| Accent | `#1F4E79` | `#6B9BC3` |
| Hairline | `#C9D3DC` | `#243140` |
| Signal | `#B87A2B` | `#D4A04A` |

---

## 3. Atelier Bone + Oxide

**Vibe:** Print atelier / architecture folio — warm bone paper, charcoal type, oxide red as rare punctuation.  
Warm without terracotta cliché; accent used like a stamp, not a theme wash.

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#F7F3EB` | `#1A1714` |
| Ink | `#24201C` | `#F0E9DF` |
| Accent | `#8C3B2E` | `#C46A55` |
| Secondary | `#5C6B5A` | `#8FA392` |
| Hairline | `#E0D8CC` | `#322C26` |

---

## 4. Observatory Ink + Ion

**Vibe:** Scientific instrument panel — near-black ink, cold paper, precise ion cyan (not teal neon).  
Closest to the prior Ledger Noir lineage, but cleaner and less “stock dark UI.”

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#F5F7F9` | `#0A0E12` |
| Ink | `#0E1419` | `#E6EEF2` |
| Accent | `#0B6E7A` | `#3DB8C5` |
| Hairline | `#D2DAE0` | `#1C252D` |
| Ok | `#2F6B4F` | `#5FA882` |

---

## 5. Kyoto Ledger + Matcha Iron

**Vibe:** Japanese stationery + iron tools — soft washi, iron black, muted matcha, ink-red sparingly.  
Calm, distinctive, high craft — strong brand test if type is also considered.

| Token | Light | Dark |
| --- | --- | --- |
| Canvas | `#F4F2EC` | `#141513` |
| Ink | `#1C1C1A` | `#ECEAE4` |
| Accent | `#4A5D45` | `#8FA88A` |
| Mark | `#8B3A3A` | `#C47A7A` |
| Hairline | `#DED9CF` | `#2B2C28` |

---

## Recommendation

Start with **1 Graphite + Verdigris** or **4 Observatory Ink + Ion** — both scale cleanly across ops pages; 1 feels more premium, 4 more “instrument.”

**Avoid for this product:** purple gradients, heavy glow, candy pills, balance-as-hero gold.

---

## Status

- [x] Palette chosen: **Kyoto Ledger + Matcha Iron**
- [x] CSS variables locked for light + dark (`design/tokens.css`)
- [ ] Homepage restyled as proof surface
- [ ] Roll out to other pages from that base
- [ ] Theme toggle UI (`data-theme="light|dark"` ready)
