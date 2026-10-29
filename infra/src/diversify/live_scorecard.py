"""
Live scorecard — backtest (SHADOW vs CURRENT) + portfolio combination + live forward test.

Reads run_p2_scorer outputs (SCORECARD.json + sleeves/*_live_fire_tape.csv):
  artefacts/live_scorecard/BT_SHADOW   offline backtest of the LIVE-SHADOW presets (scorecard basis)
  artefacts/live_scorecard/BT_CURRENT  same window, exact current live inputs (LIVE_WITHHOLD) for comparison
  artefacts/live_scorecard/LIVE        optional — forward test, from run_p2_scorer on VPS hosting logs

Usage (from infra/):
  python -m src.diversify.live_scorecard
New symbols: add a LiveRunCard in live_runs.py, back-test its LIVE-SHADOW preset into BT_SHADOW, re-run.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .live_runs import LIVE_RUNS, by_asset

INFRA = Path(__file__).resolve().parents[2]
BASE = INFRA / "artefacts" / "live_scorecard"
VARIANTS = {"SHADOW": BASE / "BT_SHADOW", "CURRENT": BASE / "BT_CURRENT", "LIVE": BASE / "LIVE"}
RISK_PCT = {c.asset_id: c.risk_pct for c in LIVE_RUNS}
CARDS = by_asset()
BASE_RISK = 0.5
GO_LIVE = "2026-10-29 17:19"  # VPS migration of the deployed presets + EA 1.28 (forward-test start)
GROUPS = {"GRP primary JP225+DE40": ["JP225", "DE40"]}


def _load(variant_dir: Path) -> tuple[dict, dict[str, pd.DataFrame]] | None:
    card_path = variant_dir / "SCORECARD.json"
    if not card_path.exists():
        return None
    card = json.loads(card_path.read_text(encoding="utf-8"))
    tapes = {}
    for aid in card["sleeve_summary"]:
        df = pd.read_csv(variant_dir / "sleeves" / f"{aid}_live_fire_tape.csv")
        df["close_dt"] = pd.to_datetime(df["close_time"], format="%Y.%m.%d %H:%M:%S")
        tapes[aid] = df.sort_values("close_dt").reset_index(drop=True)
    return card, tapes


def _rolling(df: pd.DataFrame, leak: float, bwr: float = 50.0) -> dict:
    win = df["win"].astype(float)
    r = df["pnl_R_design"].astype(float)
    out = {}
    for w in (20, 50):
        if len(df) < w:
            continue
        ef = win.rolling(w).mean() * 100 - bwr - leak
        en = r.rolling(w).mean()
        out[f"W{w}_EF_min"] = round(float(ef.min()), 1)
        out[f"W{w}_EF_last"] = round(float(ef.iloc[-1]), 1)
        out[f"W{w}_EN_last"] = round(float(en.iloc[-1]), 3)
        out[f"W{w}_pct_EF_le_0"] = round(100 * float((ef.dropna() <= 0).mean()), 1)
    daily = r.groupby(df["close_dt"].dt.normalize()).sum()
    r30 = daily.rolling("30D").sum()
    out["R30d_min"] = round(float(r30.min()), 2)
    out["R30d_last"] = round(float(r30.iloc[-1]), 2)
    return out


def _sleeve_rows(card: dict, tapes: dict[str, pd.DataFrame]) -> dict:
    rows = {}
    for aid, s in card["sleeve_summary"].items():
        f = s["full"]
        monthly = tapes[aid].groupby(tapes[aid]["close_dt"].dt.strftime("%Y-%m"))["pnl_R_design"].sum()
        rows[aid] = {
            "deploy": CARDS[aid].deploy if aid in CARDS else "SHADOW",
            "magic": s["magic"],
            "n": f["n"],
            "trades_per_30d": f["trades_per_30d"],
            "WR_pct": f["WR_pct"],
            "sum_R": f["sum_R"],
            "E_N": f["E_N"],
            "PF_R": f["profit_factor_R"],
            "EF_pp": f["EF_pp"],
            "EF_zone": f["EF_zone"],
            "maxDD_R": f["maxDD_R"],
            "max_loss_streak": f["max_loss_streak"],
            "CVaR_day_20": f["CVaR_day_20"],
            "month_hit": s["month_hit"],
            "quarter_hit": s["quarter_hit"],
            "worst_month": s["worst_month_id"],
            "worst_month_R": round(float(monthly.min()), 2),
            "best_month_R": round(float(monthly.max()), 2),
            "date_last": s["date_max"],
            "monthly_R": {k: round(float(v), 2) for k, v in monthly.items()},
            **_rolling(tapes[aid], float(f.get("Leak_pp") or 0.0), float(f.get("BWR") or CARDS[aid].bwr)),
        }
    return rows


def _daily_panel(tapes: dict[str, pd.DataFrame], start: str, end: str) -> pd.DataFrame:
    idx = pd.date_range(start, end, freq="D")  # calendar days: FX/index trades also close on weekends
    cols = {}
    for aid, df in tapes.items():
        d = df.groupby(df["close_dt"].dt.normalize())["pnl_R_design"].sum()
        cols[aid] = d.reindex(idx, fill_value=0.0)
    return pd.DataFrame(cols, index=idx)


def _book(panel: pd.DataFrame, weights: dict[str, float]) -> dict:
    cols = [c for c in panel.columns if c in weights]
    sub = panel[cols]
    book = (sub * pd.Series(weights)[cols]).sum(axis=1)
    eq = book.cumsum()
    monthly = book.groupby(book.index.strftime("%Y-%m")).sum()
    active = book[sub.ne(0).any(axis=1)]
    r30 = book.rolling(30).sum()
    sleeve_dd = sum(
        float((sub[c] * weights[c]).cumsum().sub((sub[c] * weights[c]).cumsum().cummax()).min()) for c in cols
    )
    book_dd = float((eq - eq.cummax()).min())
    neg = sub.lt(0)
    pos_or_neg = sub.ne(0)
    corr_vals = []
    for i, a in enumerate(cols):
        for b in cols[i + 1:]:
            both = pos_or_neg[a] & pos_or_neg[b]
            if both.sum() >= 10:
                corr_vals.append(float(np.corrcoef(sub.loc[both, a], sub.loc[both, b])[0, 1]))
    return {
        "members": cols,
        "weights": {c: weights[c] for c in cols},
        "sum_R": round(float(book.sum()), 2),
        "maxDD_R": round(book_dd, 2),
        "sum_sleeve_maxDD_R": round(sleeve_dd, 2),
        "dd_diversification_ratio": round(sleeve_dd / book_dd, 2) if book_dd < 0 else None,
        "month_hit": round(float((monthly > 0).mean()), 3),
        "worst_month_R": round(float(monthly.min()), 2),
        "best_month_R": round(float(monthly.max()), 2),
        "day_hit_rate": round(float((active > 0).mean()), 3),
        "worst_day_R": round(float(book.min()), 2),
        "CVaR_day_20": round(float(active[active <= active.quantile(0.2)].mean()), 2),
        "R30d_min": round(float(r30.min()), 2),
        "R30d_last": round(float(r30.iloc[-1]), 2),
        "max_sleeves_losing_same_day": int(neg.sum(axis=1).max()),
        "days_3plus_sleeves_losing": int((neg.sum(axis=1) >= 3).sum()),
        "avg_pairwise_corr_active": round(float(np.mean(corr_vals)), 3) if corr_vals else None,
        "monthly_R": {k: round(float(v), 2) for k, v in monthly.items()},
        "equity_by_month_end": {k: round(float(v), 2) for k, v in eq.groupby(eq.index.strftime("%Y-%m")).last().items()},
    }


def _portfolio(tapes: dict[str, pd.DataFrame], start: str, end: str) -> dict:
    panel = _daily_panel(tapes, start, end)
    aids = list(panel.columns)
    out = {
        "equal_R": _book(panel, {a: 1.0 for a in aids}),
        "live_risk_weighted": _book(panel, {a: RISK_PCT.get(a, BASE_RISK) / BASE_RISK for a in aids}),
    }
    for name, members in GROUPS.items():
        if all(m in aids for m in members):
            out[name] = _book(panel, {m: 1.0 for m in members})
    return out


def _deployed(loaded: dict) -> tuple[dict, dict[str, pd.DataFrame]] | None:
    """Per-sleeve pick of the SHADOW or CURRENT backtest according to each card's live posture."""
    if "SHADOW" not in loaded or "CURRENT" not in loaded:
        return None
    card = dict(loaded["SHADOW"][0])
    card["sleeve_summary"], tapes = {}, {}
    for aid in loaded["SHADOW"][0]["sleeve_summary"]:
        src = CARDS[aid].deploy if aid in CARDS else "SHADOW"
        card["sleeve_summary"][aid] = loaded[src][0]["sleeve_summary"][aid]
        tapes[aid] = loaded[src][1][aid]
    return card, tapes


def build() -> dict:
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "basis": "Offline Tester backtest of the deployed presets (SHADOW or CURRENT per sleeve) · designed R · EA 1.28",
        "window": None,
        "deploy": {c.asset_id: c.deploy for c in LIVE_RUNS},
        "variants": {},
    }
    loaded = {name: x for name, d in VARIANTS.items() if (x := _load(d))}
    dep = _deployed(loaded)
    order = ({"DEPLOYED": dep} if dep else {}) | loaded
    for name, (card, tapes) in order.items():
        start = card.get("close_from") or min(t["close_dt"].min() for t in tapes.values()).date().isoformat()
        end = card.get("close_to") or max(t["close_dt"].max() for t in tapes.values()).date().isoformat()
        if name in ("DEPLOYED", "SHADOW") and result["window"] is None:
            result["window"] = [start, end]
        result["variants"][name] = {
            "window": [start, end],
            "sleeves": _sleeve_rows(card, tapes),
            "portfolio": _portfolio(tapes, start, end),
        }
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / "LIVE_SCORECARD.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def _fmt(v, nd=2) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:+.{nd}f}" if nd and abs(v) < 1e6 else f"{v}"
    return str(v)


def _sleeve_table(sleeves: dict, shadow: dict | None = None, current: dict | None = None) -> list[str]:
    cmp = bool(shadow and current)
    lines = [
        "| Sleeve | Mode | n | /30d | WR % | ΣR | E_N | PF | EF pp | Zone | maxDD R | Month hit | Worst month R"
        + (" | ΣR shadow | ΣR current |" if cmp else " |"),
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---:"
        + (" | ---: | ---: |" if cmp else " |"),
    ]
    for aid, s in sorted(sleeves.items(), key=lambda kv: -kv[1]["sum_R"]):
        row = (
            f"| {aid} | {s.get('deploy', '—')} | {s['n']} | {s['trades_per_30d']:.1f} | {s['WR_pct']:.1f} | "
            f"{_fmt(s['sum_R'], 1)} | {_fmt(s['E_N'], 3)} | {s['PF_R']:.2f} | {_fmt(s['EF_pp'], 1)} | {s['EF_zone']} | "
            f"{s['maxDD_R']:.1f} | {100 * s['month_hit']:.0f}% | {_fmt(s['worst_month_R'], 1)}"
        )
        if cmp and aid in shadow and aid in current:
            row += f" | {_fmt(shadow[aid]['sum_R'], 1)} | {_fmt(current[aid]['sum_R'], 1)} |"
        else:
            row += " |"
        lines.append(row)
    return lines


def _rolling_table(sleeves: dict) -> list[str]:
    lines = [
        "| Sleeve | W20 EF min | W50 EF min | W50 EF last | W50 EN last | % bars W50 EF ≤ 0 | 30d R min | 30d R last |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for aid, s in sorted(sleeves.items()):
        lines.append(
            f"| {aid} | {_fmt(s.get('W20_EF_min'), 1)} | {_fmt(s.get('W50_EF_min'), 1)} | "
            f"{_fmt(s.get('W50_EF_last'), 1)} | {_fmt(s.get('W50_EN_last'), 3)} | "
            f"{s.get('W50_pct_EF_le_0', '—')}% | {_fmt(s['R30d_min'], 1)} | {_fmt(s['R30d_last'], 1)} |"
        )
    return lines


def _portfolio_table(port: dict) -> list[str]:
    keys = [
        ("sum_R", "ΣR"), ("maxDD_R", "maxDD R"), ("sum_sleeve_maxDD_R", "Σ sleeve maxDD R"),
        ("dd_diversification_ratio", "DD diversification ×"), ("month_hit", "Month hit"),
        ("worst_month_R", "Worst month R"), ("best_month_R", "Best month R"), ("day_hit_rate", "Day hit (active)"),
        ("worst_day_R", "Worst day R"), ("CVaR_day_20", "CVaR day 20% R"), ("R30d_min", "Worst ~30d R"),
        ("max_sleeves_losing_same_day", "Max sleeves losing same day"),
        ("days_3plus_sleeves_losing", "Days with ≥3 sleeves losing"),
        ("avg_pairwise_corr_active", "Avg pairwise daily corr"),
    ]
    names = list(port.keys())
    lines = ["| Metric | " + " | ".join(names) + " |", "| --- |" + " ---: |" * len(names)]
    for k, label in keys:
        vals = []
        for n in names:
            v = port[n].get(k)
            if k in ("month_hit", "day_hit_rate") and v is not None:
                vals.append(f"{100 * v:.0f}%")
            elif isinstance(v, float):
                vals.append(f"{v:.2f}")
            else:
                vals.append("—" if v is None else str(v))
        lines.append(f"| {label} | " + " | ".join(vals) + " |")
    return lines


def _monthly_table(variant: dict) -> list[str]:
    sleeves = variant["sleeves"]
    book = variant["portfolio"]["equal_R"]["monthly_R"]
    months = sorted(book)
    aids = sorted(sleeves)
    lines = ["| Month | " + " | ".join(aids) + " | **Book (equal R)** |", "| --- |" + " ---: |" * (len(aids) + 1)]
    for m in months:
        cells = [_fmt(sleeves[a]["monthly_R"].get(m, 0.0), 1) for a in aids]
        lines.append(f"| {m} | " + " | ".join(cells) + f" | **{_fmt(book[m], 1)}** |")
    return lines


def write_md(result: dict, path: Path) -> None:
    v = result["variants"]
    dep, sh, cur, live = v.get("DEPLOYED"), v.get("SHADOW"), v.get("CURRENT"), v.get("LIVE")
    base = dep or sh
    w = result["window"] or ["?", "?"]
    eq = base["portfolio"]["equal_R"]
    shadow_ids = [a for a, m in result["deploy"].items() if m == "SHADOW"]
    current_ids = [a for a, m in result["deploy"].items() if m == "CURRENT"]
    md = [
        "# Live scorecard",
        "",
        f"**Generated:** {result['generated_utc'][:16]}Z by `infra/src/diversify/live_scorecard.py` — do not hand-edit tables; re-run the script.",
        f"**Basis:** offline MT5 Tester backtest of the **deployed presets** · {w[0]} → {w[1]} · every tick · $500 · 1:500 · EA **1.28** · designed R (SL/TP geometry).",
        f"**Deployed posture:** SHADOW (skips logged only) — {', '.join(shadow_ids)} · "
        f"CURRENT (skips enforced) — {', '.join(current_ids)}. Set per sleeve by `deploy` in `live_runs.py`.",
        "**Comparisons:** same window with every sleeve SHADOW, and every sleeve CURRENT.",
        "**Canvas:** `live-scorecard.canvas.tsx`",
        "",
        "## Summary",
        "",
        f"- Deployed book (7 sleeves, equal R): **{_fmt(eq['sum_R'], 1)}R** · maxDD **{eq['maxDD_R']:.1f}R** · "
        f"month hit **{100 * eq['month_hit']:.0f}%** · DD diversification **{eq['dd_diversification_ratio']}×** · "
        f"avg pairwise daily corr **{eq['avg_pairwise_corr_active']}**.",
    ]
    if sh and cur:
        md.append(
            f"- All-SHADOW book {_fmt(sh['portfolio']['equal_R']['sum_R'], 1)}R · all-CURRENT book "
            f"{_fmt(cur['portfolio']['equal_R']['sum_R'], 1)}R. Kept skips (AAPL, JP225, USDJPY L2det) were fitted on "
            "overlapping data → their contribution is **in-sample, optimistic**."
        )
    md += [
        "- EURUSD / UK100: no skip fired in this window (EUR L2 INF max p 0.576 < 0.606 at Tester spread 6). "
        "The Q4 calendar withhold seen live is **outside** this window.",
        "- AUDUSD at live risk 3% (6× the 0.5% sleeves) dominates live-risk-weighted drawdown.",
        "",
        "## 1. Sleeves — backtest (deployed presets)",
        "",
        *_sleeve_table(base["sleeves"], sh["sleeves"] if sh else None, cur["sleeves"] if cur else None),
        "",
        "EF pp = WR − breakeven WR − Leak (per-sleeve RR / Leak from run cards). Zone: Strong / Fragile / Below.",
        "",
        "## 2. Rolling metrics — backtest (deployed presets)",
        "",
        "W20 / W50 = rolling trade windows used by AOS L3/L4 (EF pp, E_N); 30d R = rolling calendar-30-day designed R.",
        "",
        *_rolling_table(base["sleeves"]),
        "",
        "## 3. Portfolio combination — live book as a group",
        "",
        "Daily designed-R panel (calendar days, by close date). **equal_R** = each sleeve 1R per trade; "
        "**live_risk_weighted** = R × (live risk % / 0.5%) (AUDUSD ×6); GRP primary = frozen JP225+DE40 cluster for reference. "
        "DD diversification × = Σ sleeve maxDD ÷ book maxDD (higher = more offset).",
        "",
        "### Deployed book",
        "",
        *_portfolio_table(base["portfolio"]),
        "",
    ]
    if sh and cur:
        cmp = {"deployed": base["portfolio"]["equal_R"], "all SHADOW": sh["portfolio"]["equal_R"],
               "all CURRENT": cur["portfolio"]["equal_R"]}
        md += ["### Book comparison (equal R)", "", *_portfolio_table(cmp), ""]
    md += ["### Monthly R (deployed presets)", "", *_monthly_table(base), ""]
    md += ["## 4. Live forward test", ""]
    if live:
        lw = live["window"]
        md += [
            f"Window {lw[0]} → {lw[1]} · VPS hosting logs · same metrics as backtest.",
            "",
            *_sleeve_table(live["sleeves"]),
            "",
            *_portfolio_table(live["portfolio"]),
            "",
        ]
    else:
        md += [
            f"**Status: running since {GO_LIVE} (VPS, server+1)** — no scored closes yet; run the update procedure below.",
            "",
        ]
    md += [
        "Update procedure (from `infra/`):",
        "",
        "```bat",
        "python -m src.diversify.run_p2_scorer --log ..\\..\\..\\..\\logs\\hosting.6917926.experts "
        "--from <go-live YYYY-MM-DD> --out artefacts\\live_scorecard\\LIVE --archive ..\\blotter\\archive\\LIVE-SCORECARD-LIVE",
        "python -m src.diversify.live_scorecard",
        "```",
        "",
        "## 5. Adding symbols",
        "",
        "1. Add a `LiveRunCard` (magic, RR, BWR, Leak, `risk_pct`) to `infra/src/diversify/live_runs.py`.",
        "2. Generate its LIVE-SHADOW preset (`blotter/archive/LIVE-SHADOW-PRESETS/_make_presets.py` from a VPS input dump).",
        "3. Back-test it on the scorecard window into the same log, re-run `run_p2_scorer --out artefacts\\live_scorecard\\BT_SHADOW`, then `live_scorecard`.",
        "",
        "## Sources",
        "",
        "- Backtest logs: `blotter/archive/LIVE-SHADOW-PRESETS/tester_{SHADOW,CURRENT}_v128.log`",
        "- Scored artefacts: `infra/artefacts/live_scorecard/BT_SHADOW`, `BT_CURRENT`, `LIVE_SCORECARD.json`",
        "- Presets: `Presets/LIVE-SHADOW_*.set` (full 120 inputs from VPS dump 2026-10-28 23:00)",
    ]
    path.write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    r = build()
    write_md(r, INFRA.parent / "doc" / "LIVE_SCORECARD.md")
    for v, body in r["variants"].items():
        p = body["portfolio"]["equal_R"]
        print(v, body["window"], "book sum_R", p["sum_R"], "maxDD", p["maxDD_R"], "month_hit", p["month_hit"])
