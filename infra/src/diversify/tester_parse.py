"""Parse Tester / hosting expert journals into per-magic trade events.

One long run is enough: close_date on each trade lets rolling.py slice
month / quarter / year without re-testing.

Tester journals often omit `BMRG (SYM,TF)` on TRADE lines — symbol/tf come
from the run header (`EURUSD,M5: testing of …`).
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from .live_runs import LiveRunCard, by_broker_symbol, by_magic

OPEN_RE = re.compile(
    r"\[BMRG\]\[TRADE\] OPEN (BUY|SELL)\s+"
    r"lot=([\d.]+)\s+price=([\d.]+)\s+sl=([\d.]+)\s+tp=([\d.]+)"
    r"(?:.*?spread=(\d+))?(?:.*?deal=(\d+))?",
    re.I,
)
CLOSE_RE = re.compile(r"AOS close (TP|SL|MID)\b", re.I)
BASKET_CLOSE_RE = re.compile(r"\[BMRG\]\[TRADE\] CLOSE\b", re.I)
CHART_RE = re.compile(r"BMRG \(([^,]+),([^)]+)\)")
DT_RE = re.compile(r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2})")
TIME_ONLY_RE = re.compile(r"\t(\d{2}):(\d{2}):(\d{2})\.\d+\t")
MAGIC_RE = re.compile(r"InpMagic=(\d+)")
# EURUSD,M5 (YWO-Trade): testing of Experts\BMRG\BMRG.ex5 from 2025.10.01 00:00 to 2026.10.20 00:00
RUN_HEADER_RE = re.compile(
    r"([A-Za-z0-9]+),(M\d+)(?:\s*\([^)]*\))?:\s*testing of Experts\\BMRG\\BMRG\.ex5"
    r"\s+from\s+(\S+)\s+\S+\s+to\s+(\S+)",
    re.I,
)
# fallback without symbol
RUN_START_RE = re.compile(
    r"testing of Experts\\BMRG\\BMRG\.ex5\s+from\s+(\S+)\s+.*?to\s+(\S+)",
    re.I,
)
TP_TRIG_RE = re.compile(r"take profit triggered", re.I)
SL_TRIG_RE = re.compile(r"stop loss triggered", re.I)
FNAME_DATE_RE = re.compile(r"(20\d{6})")


class RunChunk(NamedTuple):
    magic: int | None
    symbol: str | None
    tf: str | None
    window: str
    text: str


@dataclass
class ParsedTrade:
    asset_id: str
    magic: int
    symbol: str
    tf: str
    side: str
    open_time: datetime
    close_time: datetime
    entry: float
    sl: float
    tp: float
    exit_reason: str
    pnl_R_design: float
    spread_pts: int | None
    deal: str | None
    lot: float


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def design_pnl_R(side: str, entry: float, sl: float, tp: float, exit_reason: str) -> float:
    side_u = side.upper()
    if side_u == "BUY":
        risk = abs(entry - sl)
        reward = abs(tp - entry)
    else:
        risk = abs(sl - entry)
        reward = abs(entry - tp)
    reason = exit_reason.upper()
    if reason == "TP":
        return (reward / risk) if risk > 0 else 1.0
    if reason == "SL":
        return -1.0
    return 0.0


def _line_dt(
    line: str,
    fallback: datetime | None,
    *,
    file_day: datetime | None = None,
) -> datetime | None:
    m = DT_RE.search(line)
    if m:
        return datetime.strptime(m.group(1), "%Y.%m.%d %H:%M:%S")
    tm = TIME_ONLY_RE.search(line)
    if tm and file_day is not None:
        return file_day.replace(
            hour=int(tm.group(1)),
            minute=int(tm.group(2)),
            second=int(tm.group(3)),
            microsecond=0,
        )
    return fallback


def _file_day_from_path(path: Path) -> datetime | None:
    m = FNAME_DATE_RE.search(path.name)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y%m%d")


def _line_chart(line: str) -> tuple[str, str] | None:
    m = CHART_RE.search(line)
    if not m:
        return None
    return m.group(1), m.group(2)


def _alias_asset(sym: str) -> str:
    return (
        sym.replace("Apple", "AAPL")
        .replace("DE30", "DE40")
        .replace("JPN225", "JP225")
    )


def parse_run_chunks(text: str) -> list[RunChunk]:
    """Split Tester log into runs with symbol/tf/magic from headers."""
    headers = list(RUN_HEADER_RE.finditer(text))
    if not headers:
        # hosting / odd format — single blob
        starts = list(RUN_START_RE.finditer(text))
        if not starts:
            return [RunChunk(None, None, None, "whole_log", text)]
        out: list[RunChunk] = []
        for i, m in enumerate(starts):
            end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
            chunk = text[m.start() : end]
            mm = MAGIC_RE.search(chunk[:20000])
            out.append(
                RunChunk(
                    int(mm.group(1)) if mm else None,
                    None,
                    None,
                    f"{m.group(1)}->{m.group(2)}",
                    chunk,
                )
            )
        return out

    out = []
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        chunk = text[m.start() : end]
        mm = MAGIC_RE.search(chunk[:25000])
        sym, tf = m.group(1), m.group(2)
        out.append(
            RunChunk(
                int(mm.group(1)) if mm else None,
                sym,
                tf,
                f"{m.group(3)}->{m.group(4)}",
                chunk,
            )
        )
    return out


def parse_trades_from_text(
    text: str,
    *,
    default_magic: int | None = None,
    default_asset: str | None = None,
    default_symbol: str | None = None,
    default_tf: str | None = None,
    file_day: datetime | None = None,
) -> list[ParsedTrade]:
    """Walk OPEN → close pairs; map symbol/magic via live run cards."""
    mag_map = by_magic()
    sym_map = by_broker_symbol()
    trades: list[ParsedTrade] = []

    # single pending open (Tester is one symbol per run); also key by chart if present
    pending_single: dict | None = None
    pending_chart: dict[tuple[str, str], dict] = {}
    last_dt: datetime | None = None
    run_magic = default_magic

    for line in text.splitlines():
        dt = _line_dt(line, last_dt, file_day=file_day)
        if dt is not None and (DT_RE.search(line) or TIME_ONLY_RE.search(line)):
            last_dt = dt

        mm = MAGIC_RE.search(line)
        if mm:
            run_magic = int(mm.group(1))

        chart = _line_chart(line)
        om = OPEN_RE.search(line)
        if om and dt:
            rec = {
                "side": om.group(1).upper(),
                "lot": float(om.group(2)),
                "entry": float(om.group(3)),
                "sl": float(om.group(4)),
                "tp": float(om.group(5)),
                "spread": int(om.group(6)) if om.group(6) else None,
                "deal": om.group(7),
                "open_time": dt,
                "magic": run_magic or default_magic,
                "sym": chart[0] if chart else default_symbol,
                "tf": chart[1] if chart else default_tf,
            }
            if chart:
                pending_chart[chart] = rec
            else:
                pending_single = rec
            continue

        reason = None
        cm = CLOSE_RE.search(line)
        if cm:
            reason = cm.group(1).upper()
        elif TP_TRIG_RE.search(line):
            reason = "TP"
        elif SL_TRIG_RE.search(line):
            reason = "SL"
        elif BASKET_CLOSE_RE.search(line):
            continue

        if reason is None or dt is None:
            continue

        o = None
        if chart and chart in pending_chart:
            o = pending_chart.pop(chart)
        elif pending_single is not None:
            o = pending_single
            pending_single = None
        elif len(pending_chart) == 1:
            # rare: close without chart tag
            key = next(iter(pending_chart))
            o = pending_chart.pop(key)
        if o is None:
            continue

        magic = o.get("magic") or default_magic
        sym = o.get("sym") or default_symbol or "?"
        tf = o.get("tf") or default_tf or "?"
        card: LiveRunCard | None = None
        # Prefer magic identity (live sleeve) over chart symbol — catches mis-attaches
        if magic in mag_map:
            card = mag_map[magic]
        elif sym in sym_map:
            card = sym_map[sym]
            magic = card.magic
        asset_id = (
            card.asset_id
            if card
            else (default_asset or _alias_asset(sym))
        )
        if magic is None:
            magic = 0

        pnl = design_pnl_R(o["side"], o["entry"], o["sl"], o["tp"], reason)
        trades.append(
            ParsedTrade(
                asset_id=asset_id,
                magic=int(magic),
                symbol=sym,
                tf=tf,
                side=o["side"],
                open_time=o["open_time"],
                close_time=dt,
                entry=o["entry"],
                sl=o["sl"],
                tp=o["tp"],
                exit_reason=reason,
                pnl_R_design=round(pnl, 6),
                spread_pts=o.get("spread"),
                deal=o.get("deal"),
                lot=o["lot"],
            )
        )

    return trades


def _chunk_window_bounds(window: str) -> tuple[str | None, str | None]:
    """Parse 'YYYY.MM.DD->YYYY.MM.DD' into (start, end) date strings."""
    if not window or "->" not in window:
        return None, None
    a, b = window.split("->", 1)
    return a.strip()[:10], b.strip()[:10]


def parse_log_file(
    path: Path,
    *,
    window_from: str | None = None,
    window_to: str | None = None,
) -> list[ParsedTrade]:
    """Parse Tester journal.

    If window_from / window_to are set (YYYY.MM.DD or YYYY-MM-DD), only keep
    run chunks whose Tester header window matches both bounds. Use this for a
    clean tip panel when the same log also holds longer passes.
    """
    text = load_text(path)
    file_day = _file_day_from_path(path)
    all_trades: list[ParsedTrade] = []
    run_meta: list[dict] = []
    wf = window_from.replace("-", ".")[:10] if window_from else None
    wt = window_to.replace("-", ".")[:10] if window_to else None
    for chunk in parse_run_chunks(text):
        w_start, w_end = _chunk_window_bounds(chunk.window)
        skipped = False
        if wf is not None or wt is not None:
            if (wf is not None and w_start != wf) or (wt is not None and w_end != wt):
                skipped = True
        asset = None
        if chunk.magic and chunk.magic in by_magic():
            asset = by_magic()[chunk.magic].asset_id
        elif chunk.symbol:
            asset = _alias_asset(chunk.symbol)
        trades = parse_trades_from_text(
            chunk.text,
            default_magic=chunk.magic,
            default_asset=asset,
            default_symbol=chunk.symbol,
            default_tf=chunk.tf,
            file_day=file_day,
        )
        run_meta.append(
            {
                "magic": chunk.magic,
                "symbol": chunk.symbol,
                "tf": chunk.tf,
                "window": chunk.window,
                "n_trades": len(trades),
                "asset_id": asset,
                "skipped_window": skipped,
                "mismatch": bool(
                    chunk.magic
                    and chunk.symbol
                    and chunk.magic in by_magic()
                    and by_magic()[chunk.magic].broker_symbol != chunk.symbol
                    and not (
                        by_magic()[chunk.magic].broker_symbol == "Apple"
                        and chunk.symbol == "Apple"
                    )
                    and by_magic()[chunk.magic].broker_symbol != chunk.symbol
                ),
            }
        )
        # refine mismatch: compare expected broker symbol
        if chunk.magic and chunk.magic in by_magic() and chunk.symbol:
            exp = by_magic()[chunk.magic].broker_symbol
            run_meta[-1]["expected_symbol"] = exp
            run_meta[-1]["mismatch"] = exp != chunk.symbol
        if skipped:
            continue
        all_trades.extend(trades)

    # stash last parse meta on function attribute for callers
    parse_log_file.last_run_meta = run_meta  # type: ignore[attr-defined]

    # Dedupe across overlapping Tester windows (same trade replayed in tip +
    # long runs). Deal ids restart per run — use open/close/side/entry identity.
    seen: set[tuple] = set()
    uniq: list[ParsedTrade] = []
    for t in all_trades:
        key = (
            t.magic,
            t.side,
            t.open_time.isoformat(timespec="seconds"),
            t.close_time.isoformat(timespec="seconds"),
            round(t.entry, 8),
            round(t.sl, 8),
            round(t.tp, 8),
        )
        if key in seen:
            continue
        seen.add(key)
        uniq.append(t)
    return uniq


def trades_to_fire_rows(trades: list[ParsedTrade]) -> list[dict]:
    """Minimal fire-tape rows compatible with diversify.load._load_fire_tape."""
    rows = []
    for t in trades:
        rows.append(
            {
                "open_time": t.open_time.strftime("%Y.%m.%d %H:%M:%S"),
                "close_time": t.close_time.strftime("%Y.%m.%d %H:%M:%S"),
                "side": t.side,
                "lot": t.lot,
                "entry": t.entry,
                "sl": t.sl,
                "tp": t.tp,
                "spread_pts": t.spread_pts if t.spread_pts is not None else "",
                "exit_reason": t.exit_reason,
                "win": 1 if t.pnl_R_design > 0 else 0,
                "pnl_R_design": t.pnl_R_design,
                "magic": t.magic,
                "symbol": t.symbol,
                "tf": t.tf,
                "asset_id": t.asset_id,
                "deal": t.deal or "",
            }
        )
    return rows


def trade_asdict(t: ParsedTrade) -> dict:
    d = asdict(t)
    d["open_time"] = t.open_time.isoformat()
    d["close_time"] = t.close_time.isoformat()
    return d
