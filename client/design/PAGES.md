# Pages — BMRG operator console

**Purpose:** Living map of forward-facing pages and sections. Update when we add or delete.  
**Audience:** Operators / researchers / viewers — product language only.  
**Rule:** Do not surface internal pipelines, layer IDs, artefact paths, or wiring guts in the UI copy described here.

**Companions:** `client/design/APP_THEME.md` · `doc/client_product_brief.md` · `doc/project_report.md`

---

## Status legend

| Status | Meaning |
| --- | --- |
| **planned** | In this map; not built (or stripped for redesign) |
| **shell** | Route/chrome exists; sections not filled |
| **active** | Sections in use |
| **removed** | Dropped from the product map |

---

## Five main pages

| # | Page | Nav label | Job (operator) | Status |
| --- | --- | --- | --- | --- |
| 1 | **Home** | Home | One glance: is the champion healthy, and what should I do next? | active |
| 2 | **Performance** | Performance | Is the book’s edge score acceptable across windows? | active |
| 3 | **Live desk** | Live | What is attached and running on the chart right now? | active |
| 4 | **Review** | Review | Why were entries allowed or held back — and was the prove honest? | active |
| 5 | **Records** | Records | Where are run notes, archives, presets, and forward-test prep? | active |

Former sprawl (Health / Layers / Prove / Ops / Blotter / FT) collapses into these five. Functionality can deepen later without growing the nav.

Shell nav (Home · Performance · Live · Review · Records) under Kyoto Ledger chrome is **active**.

---

## Page 1 — Home

**Intent:** Single composition, not a dashboard.

| # | Section | Shows (product) | Status |
| --- | --- | --- | --- |
| 1 | Brand frame | Product name / console frame | active |
| 2 | Champion strip | Which strategy is active (name · account kind · version) | active |
| 3 | Edge snapshot | Core edge metrics only (no vanity balance) | active |
| 4 | Protection posture | Allow / hold / halt in plain language | active |
| 5 | Next action | One clear operational step | active |
| 6 | Recent pulse | Last meaningful update (attach, halt, or review note) | active |

---

## Page 2 — Performance

**Intent:** Score the book the way the edge framework speaks — windows and accept posture.

| # | Section | Shows (product) | Status |
| --- | --- | --- | --- |
| 1 | Edge scorecard | Primary edge metrics for the selected window | active |
| 2 | Window switcher | Long · stress · year-to-date (as available) | active |
| 3 | Vs reference | How current scores sit vs the locked champion reference | active |
| 4 | Accept posture | Pass / warn / fail on sample, edge floor, drawdown slack, activity | active |
| 5 | Activity cadence | Expected vs recent fire/basket pace (operator-facing) | active |
| 6 | Caveats | Path honesty notes (e.g. paper lift ≠ live equity) | active |

---

## Page 3 — Live desk

**Intent:** Observe the attached expert — never trade from the browser.

| # | Section | Shows (product) | Status |
| --- | --- | --- | --- |
| 1 | Attachment | Symbol · timeframe · preset role · version | active |
| 2 | Run mode | Off / observe-only / live-hold (plain labels) | active |
| 3 | Safety strip | Equity / daily / hard-stop / pause / size posture | active |
| 4 | Open book | Basket side · entries · exposure (read-only) | active |
| 5 | Journal | Recent operator-relevant lines (bars, signals, halts) | active |
| 6 | Desk notices | Kill is chart-side only · no remote order controls | active |

---

## Page 4 — Review

**Intent:** Audit decisions and honesty of prove — without exposing model plumbing.

| # | Section | Shows (product) | Status |
| --- | --- | --- | --- |
| 1 | Decision feed | Allowed vs held-back entries with short reasons | active |
| 2 | Protection map | What protections are on / paper / offline (plain) | active |
| 3 | Paper vs live | Clear separation: offline prove lift is not live equity | active |
| 4 | Verdict timeline | Accept / reject / go history for recent reviews | active |
| 5 | Size & halt story | When size was reduced or new entries stopped | active |
| 6 | Export | Download review packet (scores / decisions) for archive | active |

---

## Page 5 — Records

**Intent:** Close the loop on runs, presets, and forward-test readiness.

| # | Section | Shows (product) | Status |
| --- | --- | --- | --- |
| 1 | Current pointer | What was last reviewed and where it lives | active |
| 2 | Inbox | Unprocessed drops for the active task | active |
| 3 | Archive | Past task folders and verdicts | active |
| 4 | Preset library | Named setups and champion roles (no internal IDs required in UI) | active |
| 5 | Forward-test prep | Attach checklist + programme metrics (mutate gated) | active |
| 6 | Review checklist | Clear-after-review assist (archive · clear · update pointer) | active |

---

## Explicitly not pages (for now)

| Idea | Why not a top-level page |
| --- | --- |
| Separate “layers / OS stack” | Folded into Review → Protection map |
| Separate “prove / CF” | Folded into Review → Paper vs live + Verdicts |
| Separate “ops / pins / jobs” | Backend concern; surface outcomes in Review/Records later if needed |
| Separate “FT ship” | Stays a gated block inside Records → Forward-test prep |
| Trading / order ticket | Hard non-goal |

---

## Change log

| Date | Change |
| --- | --- |
| 2026-10-04 | Initial map — 5 pages × 6 sections; prior multi-route IA superseded for product nav |
| 2026-10-04 | Shell nav + five routes active; Home · Performance · Live · Review · Records sections marked active (Kyoto Ledger) |
