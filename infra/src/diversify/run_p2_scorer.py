"""
DIV-P2 live-preset scorer — long Tester journal → tape + rolling M/Q/Y metrics.

Usage (from infra/):
  python -m src.diversify.run_p2_scorer
  python -m src.diversify.run_p2_scorer --log path\\to\\20261021.log
  python -m src.diversify.run_p2_scorer --log a.log --log b.log
  python -m src.diversify.run_p2_scorer --inbox

Drop Tester logs into blotter/inbox/ (*.log) or pass --log.
One 12m run per live preset is enough — scorer segments months/quarters/years.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

from .live_runs import LIVE_RUNS, cards_dict
from .rolling import flatten_period_rows, hit_matrix, segment
from .tester_parse import parse_log_file, trades_to_fire_rows


def _parse_ymd(s: str | None) -> date | None:
    if not s:
        return None
    return date.fromisoformat(s.replace(".", "-"))

REPO = Path(__file__).resolve().parents[3]
OUT_LATEST = REPO / "infra" / "artefacts" / "diversify" / "P2_LATEST"
ARCHIVE = REPO / "blotter" / "archive" / "DIV-P2-T01"
INBOX = REPO / "blotter" / "inbox"
DEFAULT_TESTER = (
    REPO.parent.parent.parent / "Tester" / "logs"
)  # Terminal/.../Tester/logs


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=True), encoding="utf-8")


def _discover_logs(explicit: list[Path], use_inbox: bool) -> list[Path]:
    found: list[Path] = []
    for p in explicit:
        if p.is_file():
            found.append(p)
        elif p.is_dir():
            found.extend(sorted(p.glob("*.log")))
    if use_inbox and INBOX.exists():
        found.extend(sorted(INBOX.glob("*.log")))
    # de-dupe
    uniq: list[Path] = []
    seen: set[str] = set()
    for p in found:
        k = str(p.resolve()).lower()
        if k in seen:
            continue
        seen.add(k)
        uniq.append(p)
    return uniq


def _write_fire_tape(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # stable column union
    cols: list[str] = []
    seen: set[str] = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def run(
    logs: list[Path],
    *,
    close_from: date | None = None,
    close_to: date | None = None,
    match_tester_window: bool = False,
    out_latest: Path = OUT_LATEST,
    archive: Path = ARCHIVE,
) -> dict:
    if not logs:
        raise SystemExit(
            "No logs found. Pass --log <Tester\\logs\\YYYYMMDD.log> or drop "
            "*.log into blotter/inbox/ then --inbox"
        )

    win_from = close_from.isoformat().replace("-", ".") if close_from else None
    win_to = close_to.isoformat().replace("-", ".") if close_to else None
    # Tester header end is exclusive in practice (to 2026.10.20 = last bar 10.19);
    # keep exact header match when match_tester_window is set.
    all_trades = []
    run_meta_all: list[dict] = []
    for p in logs:
        trades = parse_log_file(
            p,
            window_from=win_from if match_tester_window else None,
            window_to=win_to if match_tester_window else None,
        )
        meta = getattr(parse_log_file, "last_run_meta", []) or []
        run_meta_all.extend([{**m, "source": p.name} for m in meta])
        kept_runs = [m for m in meta if not m.get("skipped_window")]
        print(
            f"  {p.name}: {len(trades)} trades · "
            f"{len(kept_runs)}/{len(meta)} runs kept"
        )
        for m in meta:
            if m.get("skipped_window"):
                continue
            flag = " MISMATCH" if m.get("mismatch") else ""
            print(
                f"    {m.get('symbol')},{m.get('tf')} magic={m.get('magic')} "
                f"win={m.get('window')} n={m.get('n_trades')} "
                f"-> {m.get('asset_id')}{flag}"
            )
        all_trades.extend(trades)

    # Drop only trades from mismatched (magic, symbol) runs — e.g. UK100 magic
    # on USDJPY chart — without deleting correct UK100 chart runs of the same magic.
    bad_pairs = {
        (m["magic"], m["symbol"])
        for m in run_meta_all
        if m.get("mismatch") and m.get("magic") is not None and m.get("symbol")
    }
    live_magics = {c.magic for c in LIVE_RUNS}
    if bad_pairs:
        before = len(all_trades)
        all_trades = [
            t for t in all_trades if (t.magic, t.symbol) not in bad_pairs
        ]
        print(
            f"  dropped {before - len(all_trades)} trades from mismatched "
            f"pairs {sorted(bad_pairs)}"
        )
    # Keep live-book magics only (exclude engine twins mixed into same log)
    before_live = len(all_trades)
    non_live = [t for t in all_trades if t.magic not in live_magics]
    all_trades = [t for t in all_trades if t.magic in live_magics]
    if non_live:
        other = sorted({t.magic for t in non_live})
        print(
            f"  dropped {before_live - len(all_trades)} non-live-magic trades "
            f"(magics {other}) — engine/legacy twins excluded from P2 panel"
        )
    # Optional tip window when the journal still has older long runs mixed in.
    # Keep trades that both open and close inside [from, to] so pre-window
    # carries from longer Tester passes do not inflate the tip panel.
    if close_from is not None or close_to is not None:
        before_win = len(all_trades)
        kept = []
        for t in all_trades:
            o = t.open_time.date()
            c = t.close_time.date()
            if close_from is not None and (o < close_from or c < close_from):
                continue
            if close_to is not None and (o > close_to or c > close_to):
                continue
            kept.append(t)
        all_trades = kept
        print(
            f"  kept {len(all_trades)}/{before_win} trades with open+close in "
            f"[{close_from or '...'} .. {close_to or '...'}]"
        )

    by_asset: dict[str, list] = {}
    for t in all_trades:
        by_asset.setdefault(t.asset_id, []).append(t)

    rolling = segment(all_trades)
    matrix_m = hit_matrix(rolling, "M", value="rich")
    matrix_q = hit_matrix(rolling, "Q", value="rich")
    matrix_y = hit_matrix(rolling, "Y", value="rich")
    flat_m = flatten_period_rows(rolling, "M")
    flat_q = flatten_period_rows(rolling, "Q")
    flat_y = flatten_period_rows(rolling, "Y")

    out_latest.mkdir(parents=True, exist_ok=True)
    sleeves_dir = out_latest / "sleeves"
    sleeves_dir.mkdir(exist_ok=True)

    sleeve_summary = {}
    for aid, rows in sorted(by_asset.items()):
        fire = trades_to_fire_rows(rows)
        _write_fire_tape(sleeves_dir / f"{aid}_live_fire_tape.csv", fire)
        sl = rolling.get(aid, {})
        full = sl.get("full") or {}
        sleeve_summary[aid] = {
            "n": len(rows),
            "magic": rows[0].magic,
            "date_min": min(t.close_time for t in rows).date().isoformat(),
            "date_max": max(t.close_time for t in rows).date().isoformat(),
            "full": full,
            "month_hit": sl.get("periods", {}).get("M", {}).get("hit_rate"),
            "quarter_hit": sl.get("periods", {}).get("Q", {}).get("hit_rate"),
            "year_hit": sl.get("periods", {}).get("Y", {}).get("hit_rate"),
            "month_CVaR_20": sl.get("periods", {}).get("M", {}).get("CVaR_period_20"),
            "quarter_CVaR_20": sl.get("periods", {}).get("Q", {}).get("CVaR_period_20"),
            "month_mean_E_N": sl.get("periods", {}).get("M", {}).get("mean_E_N"),
            "quarter_mean_E_N": sl.get("periods", {}).get("Q", {}).get("mean_E_N"),
            "worst_month_id": sl.get("periods", {}).get("M", {}).get("worst_period_id"),
            "worst_quarter_id": sl.get("periods", {}).get("Q", {}).get("worst_period_id"),
            "trailing_30d": sl.get("trailing_30d"),
            "trailing_90d": sl.get("trailing_90d"),
            "trailing_365d": sl.get("trailing_365d"),
            "tape": f"sleeves/{aid}_live_fire_tape.csv",
        }

    generated = datetime.now(timezone.utc).isoformat()
    scorecard = {
        "task_id": archive.name,
        "generated_utc": generated,
        "roadmap": "doc/diversification_roadmap.md",
        "caveat": (
            "Live-preset Tester (or hosting) journal parse. Designed R from "
            "SL/TP geometry. Leak in EF_pp is profile/prior meta — deal-measured "
            "costs still OPEN. Segmenting a long run into M/Q/Y does not require "
            "re-testing per period."
        ),
        "close_from": close_from.isoformat() if close_from else None,
        "close_to": close_to.isoformat() if close_to else None,
        "match_tester_window": match_tester_window,
        "sources": [str(p) for p in logs],
        "run_cards": cards_dict(),
        "tester_runs": run_meta_all,
        "mismatched_runs": [m for m in run_meta_all if m.get("mismatch")],
        "n_trades_total": len(all_trades),
        "sleeves_found": sorted(by_asset.keys()),
        "sleeves_expected": [c.asset_id for c in LIVE_RUNS],
        "missing": [c.asset_id for c in LIVE_RUNS if c.asset_id not in by_asset],
        "metrics_schema": "doc/DIV_P2_RUNCARD.md § metrics pack",
        "sleeve_summary": sleeve_summary,
        "rolling": rolling,
        "hit_matrix_month": matrix_m,
        "hit_matrix_quarter": matrix_q,
        "hit_matrix_year": matrix_y,
    }

    _write_json(out_latest / "SCORECARD.json", scorecard)
    _write_json(out_latest / "ROLLING.json", rolling)
    _write_json(out_latest / "HIT_MATRIX_M.json", matrix_m)
    _write_json(out_latest / "HIT_MATRIX_Q.json", matrix_q)
    _write_json(out_latest / "HIT_MATRIX_Y.json", matrix_y)
    _write_json(out_latest / "RUN_CARDS.json", cards_dict())
    _write_csv(out_latest / "PERIOD_TABLE_M.csv", flat_m)
    _write_csv(out_latest / "PERIOD_TABLE_Q.csv", flat_q)
    _write_csv(out_latest / "PERIOD_TABLE_Y.csv", flat_y)

    # archive copy
    archive.mkdir(parents=True, exist_ok=True)
    for name in (
        "SCORECARD.json",
        "ROLLING.json",
        "HIT_MATRIX_M.json",
        "HIT_MATRIX_Q.json",
        "HIT_MATRIX_Y.json",
        "RUN_CARDS.json",
        "PERIOD_TABLE_M.csv",
        "PERIOD_TABLE_Q.csv",
        "PERIOD_TABLE_Y.csv",
    ):
        src = out_latest / name
        if src.exists():
            shutil.copy2(src, archive / name)
    if sleeves_dir.exists():
        dest = archive / "sleeves"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(sleeves_dir, dest)

    win_note = ""
    if close_from or close_to or match_tester_window:
        win_note = (
            f"**panel:** {close_from or '...'} → {close_to or '...'} "
            f"(match_tester_window={match_tester_window})"
        )
    review = [
        f"# {archive.name} — Live-preset long-run scorer",
        "",
        f"**generated_utc:** {generated}",
        f"**sources:** {', '.join(p.name for p in logs)}",
        f"**trades:** {len(all_trades)}",
        f"**sleeves:** {', '.join(sorted(by_asset.keys())) or '(none)'}",
        *([win_note, ""] if win_note else []),
        "## How segmentation works",
        "",
        "One Tester window per live preset is enough (tip 6m or longer).",
        "Each closed trade keeps `close_time`; the scorer buckets into calendar",
        "months / quarters / years and trailing 30/90/365d — no per-month re-run.",
        "Use `--match-tester-window` with `--from/--to` when the journal also",
        "contains older longer passes.",
        "",
        "## Sleeve rollup",
        "",
        "| Asset | n | month_hit | q_hit | full E_N | full EF | maxDD_R | worst_month |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for aid, s in sorted(sleeve_summary.items()):
        full = s.get("full") or {}
        review.append(
            f"| {aid} | {s['n']} | {s.get('month_hit')} | {s.get('quarter_hit')} | "
            f"{full.get('E_N')} | {full.get('EF_pp')} | {full.get('maxDD_R')} | "
            f"{s.get('worst_month_id')} |"
        )
    review += [
        "",
        "## Artefact tables",
        "",
        "- `ROLLING.json` — full metrics pack per sleeve × M/Q/Y + trailing 30/60/90/180/365d",
        "- `PERIOD_TABLE_{M,Q,Y}.csv` — flat rows for notebooks / cluster features",
        "- `HIT_MATRIX_{M,Q,Y}.json` — rich cell: sum_R · E_N · WR · EF · maxDD · streak",
    ]
    missing = scorecard["missing"]
    if missing:
        review += ["", f"**Missing expected sleeves:** {', '.join(missing)}"]
    if missing:
        next_steps = [
            "1. Finish remaining live-preset tip runs (see RUN_CARDS.json).",
            "2. Re-run this scorer until `missing` is empty.",
            "3. `python -m src.diversify.run_mvp` after swapping manifest tapes (P2-T02).",
        ]
    else:
        next_steps = [
            "1. Tip panel complete (7/7).",
            "2. P2-T02: point `manifest.py` tapes at `P2_LATEST/sleeves/*_live_fire_tape.csv`.",
            "3. `python -m src.diversify.run_mvp` then `run_p1` for cluster / adverse dependence.",
        ]
    review += ["", "## Next", ""] + next_steps + [
        "",
        f"Artefacts: `{out_latest.relative_to(REPO)}/` · archive `{archive.relative_to(REPO)}/`",
    ]
    (out_latest / "REVIEW.md").write_text("\n".join(review) + "\n", encoding="utf-8")
    shutil.copy2(out_latest / "REVIEW.md", archive / "REVIEW.md")

    print(f"Wrote {out_latest}")
    print(f"Archived {archive}")
    if missing:
        print(f"Missing sleeves: {missing}")
    return scorecard


def main() -> None:
    ap = argparse.ArgumentParser(description="DIV-P2 live-preset rolling scorer")
    ap.add_argument(
        "--log",
        action="append",
        type=Path,
        default=[],
        help="Tester or hosting experts .log (repeatable)",
    )
    ap.add_argument(
        "--inbox",
        action="store_true",
        help=f"Also scan {INBOX}",
    )
    ap.add_argument(
        "--tester-dir",
        type=Path,
        default=None,
        help="Optional directory of Tester logs (*.log)",
    )
    ap.add_argument(
        "--from",
        dest="close_from",
        default=None,
        help="Keep trades with close_date >= YYYY-MM-DD (tip window)",
    )
    ap.add_argument(
        "--to",
        dest="close_to",
        default=None,
        help="Keep trades with close_date <= YYYY-MM-DD (tip window)",
    )
    ap.add_argument(
        "--match-tester-window",
        action="store_true",
        help=(
            "Only parse Tester run chunks whose header from/to equals "
            "--from/--to (clean tip panel; ignores longer passes in same log)"
        ),
    )
    ap.add_argument("--out", type=Path, default=None, help=f"Output dir (default {OUT_LATEST})")
    ap.add_argument("--archive", type=Path, default=None, help=f"Archive dir (default {ARCHIVE})")
    args = ap.parse_args()
    logs = list(args.log)
    if args.tester_dir:
        logs.append(args.tester_dir)
    # default: newest Tester log if nothing else
    discovered = _discover_logs(logs, use_inbox=args.inbox or not logs)
    if not discovered and DEFAULT_TESTER.exists():
        newest = sorted(DEFAULT_TESTER.glob("*.log"), key=lambda p: p.stat().st_mtime)
        if newest:
            print(f"Defaulting to newest Tester log: {newest[-1].name}")
            discovered = [newest[-1]]
    run(
        discovered,
        close_from=_parse_ymd(args.close_from),
        close_to=_parse_ymd(args.close_to),
        match_tester_window=args.match_tester_window,
        out_latest=args.out.resolve() if args.out else OUT_LATEST,
        archive=args.archive.resolve() if args.archive else ARCHIVE,
    )


if __name__ == "__main__":
    main()
