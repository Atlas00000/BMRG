"""DE40/DE30 M5: labeled fire tapes (long / tip-core / tip) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG_DIR = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)

SL_PTS = 7000.0
ATR_MAX = 2380.0
R_DESIGN = 1.25
BWR = 1.0 / (1.0 + R_DESIGN)
LEAK_PRIOR = 0.07
MAGIC = "26101903"
PRESET = "BMRG-M5-DE40-6M-P0_balanced_chart"
# ~$ / 1R @ 0.1 lot — label-time proxy only (SL7000 / M15 was ~5.81 @ 5000)
R_CCY = 5.81 * (7000.0 / 5000.0)

# Tester end date may be 10.18 or 10.19 — match prefix, prefer latest chunk.
WINDOWS = {
    "ytd": {
        "id": "2026.01.01-2026.10.19",
        "from_prefix": "2026.01.01",
        "to_prefix": "2026.10.",
    },
    "tip": {
        "id": "2026.05.01-2026.10.19",
        "from_prefix": "2026.05.01",
        "to_prefix": "2026.10.",
    },
    # Optional legacy long (Jan→Aug) if still present in log
    "long_aug": {
        "id": "2026.01.01-2026.08.31",
        "from_prefix": "2026.01.01",
        "to_prefix": "2026.08.",
    },
}

OURO = {
    "2025-06": "MISMATCH",
    "2025-07": "MISMATCH",
    "2025-08": "MATCH",
    "2026-01": "MATCH",
    "2026-02": "MATCH",
    "2026-03": "FRAGILE",
    "2026-04": "MATCH",
    "2026-05": "MISMATCH",
    "2026-06": "MATCH",
    "2026-07": "MATCH",
    "2026-08": "MATCH",
    "2026-09": "FRAGILE",
    "2026-10": "FRAGILE",
}

# MetaTester journal header (utf-16 Tester log)
HEADER_RE = re.compile(
    r"Tester\tDE30,M5[^\n]*from (\d{4}\.\d{2}\.\d{2}) 00:00 to (\d{4}\.\d{2}\.\d{2}) 00:00"
)
re_open = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] OPEN "
    r"(BUY|SELL) lot=([0-9.]+) price=([0-9.]+) sl=([0-9.]+) tp=([0-9.]+)"
    r".*spread=(\d+)"
)
re_bar = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[INFO\] bar="
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}).*ATR=([0-9.]+)pt BBw=([0-9.]+)%"
)
re_tp = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*take profit triggered"
)
re_sl = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*stop loss triggered"
)
re_eot = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*position closed due end of test"
)
re_halt_close = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*\[BMRG\]\[TRADE\] CLOSE basket"
)


def parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y.%m.%d %H:%M:%S")


def resolve_log() -> Path:
    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.exists():
            raise SystemExit(f"log not found: {p}")
        return p
    logs = sorted(LOG_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        raise SystemExit(f"no logs in {LOG_DIR}")
    return logs[0]


def load_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_chunk(text: str, from_prefix: str, to_prefix: str) -> str | None:
    """Return last matching DE30 M5 magic chunk for from/to prefixes."""
    headers = list(HEADER_RE.finditer(text))
    best: str | None = None
    for i, s in enumerate(headers):
        if not s.group(1).startswith(from_prefix):
            continue
        if not s.group(2).startswith(to_prefix):
            continue
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        ticks = re.search(r"DE30,M5: \d+ ticks", text[s.end() : end])
        if ticks:
            end = min(end, s.end() + ticks.end())
        else:
            tp = text.find("Test passed", s.end(), end)
            if tp != -1:
                end = tp + len("Test passed")
        chunk = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        if mag and mag.group(1) == MAGIC:
            best = chunk
    return best


def extract(chunk: str, window_id: str) -> list[dict]:
    last_bar = None
    open_t = None
    rows: list[dict] = []

    for line in chunk.splitlines():
        mb = re_bar.search(line)
        if mb:
            last_bar = {"atr": float(mb.group(3)), "bbw": float(mb.group(4))}

        mo = re_open.search(line)
        if mo:
            open_t = {
                "open_time": mo.group(1),
                "side": mo.group(2),
                "lot": float(mo.group(3)),
                "entry": float(mo.group(4)),
                "sl": float(mo.group(5)),
                "tp": float(mo.group(6)),
                "spread_pts": int(mo.group(7)),
                "atr_pts": last_bar["atr"] if last_bar else None,
                "bbw_pct": last_bar["bbw"] if last_bar else None,
            }
            continue

        for kind, rx in (
            ("TP", re_tp),
            ("SL", re_sl),
            ("HALT", re_halt_close),
            ("EOT", re_eot),
        ):
            mc = rx.search(line)
            if not (mc and open_t):
                continue
            if kind == "EOT":
                open_t = None
                break
            od = parse_dt(open_t["open_time"])
            cd = parse_dt(mc.group(1))
            hold_h = (cd - od).total_seconds() / 3600.0
            win = kind == "TP"
            pnl_r = R_DESIGN if win else -1.0
            month = od.strftime("%Y-%m")
            atr = open_t["atr_pts"]
            tag = OURO.get(month, "")
            near = int(atr is not None and atr >= 0.9 * ATR_MAX)
            dow = od.strftime("%a")
            hour = od.hour
            rows.append(
                {
                    **open_t,
                    "close_time": mc.group(1),
                    "exit_reason": kind,
                    "win": int(win),
                    "y_lose": int(not win),
                    "pnl_R_design": pnl_r,
                    "pnl_ccy_proxy": round(
                        (R_CCY * R_DESIGN) if win else -R_CCY, 4
                    ),
                    "hold_h": round(hold_h, 4),
                    "dow": dow,
                    "hour": hour,
                    "month": month,
                    "ouroboros_tag": tag,
                    "nights_held": int(hold_h >= 12),
                    "near_atr_cap": near,
                    "cell_month_feb": int(month == "2026-02"),
                    "cell_month_may": int(month == "2026-05"),
                    "cell_mismatch": int(tag == "MISMATCH"),
                    "cell_fragile": int(tag == "FRAGILE"),
                    "cell_near_atr": near,
                    "cell_buy": int(open_t["side"] == "BUY"),
                    "cell_sell": int(open_t["side"] == "SELL"),
                    "magic": int(MAGIC),
                    "symbol": "DE30",
                    "preset_id": PRESET,
                    "window": window_id,
                    "tf": "M5",
                }
            )
            open_t = None
            break
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise SystemExit(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def cost_proxy(rows: list[dict], window: str) -> dict:
    spreads = [r["spread_pts"] for r in rows]
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    return {
        "task": "DE40-M5-AOS-P1",
        "window": window,
        "magic": int(MAGIC),
        "symbol": "DE30",
        "tf": "M5",
        "n": len(rows),
        "WR": round(wr, 6),
        "BM_pp": round(bm * 100, 4),
        "E_N": round(wr * (R_DESIGN + 1.0) - 1.0, 6),
        "spread_pts_entry": {
            "median": spr_med,
            "mean": round(spr_mean, 3),
            "min": min(spreads),
            "max": max(spreads),
        },
        "atr_pts_present": sum(1 for r in rows if r["atr_pts"] is not None),
        "near_atr_cap_n": sum(r["near_atr_cap"] for r in rows),
        "SL_pts": SL_PTS,
        "ATR_max": ATR_MAX,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": LEAK_PRIOR * 100,
        "EF_prior_pp": round((bm - LEAK_PRIOR) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter. Tester entry spreads understate live ~1020 pts. "
            "Prior 7.0 pp remains Stage-1 authority until measured deals."
        ),
    }


def profile_slices(rows: list[dict], title: str) -> dict:
    def slice_stats(subset: list[dict]) -> dict:
        if not subset:
            return {"n": 0}
        n = len(subset)
        wr = sum(r["win"] for r in subset) / n
        en = sum(r["pnl_R_design"] for r in subset) / n
        return {"n": n, "WR": round(wr, 4), "E_N": round(en, 4)}

    by_side = {
        s: slice_stats([r for r in rows if r["side"] == s]) for s in ("BUY", "SELL")
    }
    by_dow = {
        d: slice_stats([r for r in rows if r["dow"] == d])
        for d in ("Mon", "Tue", "Wed", "Thu", "Fri")
    }
    by_hour = {
        str(h): slice_stats([r for r in rows if r["hour"] == h])
        for h in sorted({r["hour"] for r in rows})
    }
    by_month = {}
    for m in sorted({r["month"] for r in rows}):
        by_month[m] = slice_stats([r for r in rows if r["month"] == m])
        by_month[m]["ouroboros_tag"] = OURO.get(m, "")
    return {
        "title": title,
        "n": len(rows),
        "WR": round(sum(r["win"] for r in rows) / len(rows), 4),
        "by_side": by_side,
        "by_dow": by_dow,
        "by_hour": by_hour,
        "by_month": by_month,
        "near_atr_cap": slice_stats([r for r in rows if r["near_atr_cap"] == 1]),
        "cell_month_feb": slice_stats([r for r in rows if r["cell_month_feb"] == 1]),
        "cell_month_may": slice_stats([r for r in rows if r["cell_month_may"] == 1]),
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 4
        ),
        "med_hold_h_win": round(
            median([r["hold_h"] for r in rows if r["win"] == 1] or [0]), 4
        ),
        "med_hold_h_lose": round(
            median([r["hold_h"] for r in rows if r["win"] == 0] or [0]), 4
        ),
        "tue_n": sum(1 for r in rows if r["dow"] == "Tue"),
        "atr_missing": sum(1 for r in rows if r["atr_pts"] is None),
        "ouroboros_nonempty": sum(1 for r in rows if r["ouroboros_tag"]),
    }


def main() -> None:
    log_path = resolve_log()
    print(f"log={log_path}")
    text = load_text(log_path)
    by_name: dict[str, list[dict]] = {}

    for name, cfg in WINDOWS.items():
        chunk = find_chunk(text, cfg["from_prefix"], cfg["to_prefix"])
        if chunk is None:
            print(f"MISSING chunk {name} {cfg['from_prefix']}->{cfg['to_prefix']}*")
            continue
        # Stamp actual window id from header if present
        hm = HEADER_RE.search(chunk)
        wid = (
            f"{hm.group(1)}-{hm.group(2)}"
            if hm
            else cfg["id"]
        )
        rows = extract(chunk, wid)
        by_name[name] = rows
        print(f"{name}: n={len(rows)} window={wid}")

    if "tip" not in by_name and "ytd" not in by_name:
        raise SystemExit(
            "No DE30 M5 tip/ytd chunk (magic 26101903) in log. "
            "Re-run Tester tip May→Oct / YTD then re-run this builder."
        )

    tip = by_name.get("tip")
    ytd = by_name.get("ytd")
    # Prefer YTD as long authority; fall back to tip+prior or legacy Aug long
    long = ytd or by_name.get("long_aug")
    if long is None and tip:
        long = tip

    assert long is not None
    prior = [
        {**r, "window": "2026.01.01-2026.04.30"}
        for r in long
        if parse_dt(r["open_time"]).month <= 4
        and parse_dt(r["open_time"]).year == 2026
    ]
    tip_core = [
        {**r, "window": "2026.05.01-2026.08.31"}
        for r in (tip or long)
        if parse_dt(r["open_time"]).year == 2026
        and 5 <= parse_dt(r["open_time"]).month <= 8
    ]
    sep_oct = [
        {**r, "window": "2026.09.01-2026.10.19"}
        for r in (tip or long)
        if parse_dt(r["open_time"]).year == 2026
        and parse_dt(r["open_time"]).month >= 9
    ]

    write_csv(OUT / "de40_m5_ytd_fire_tape.csv", long)
    write_csv(OUT / "de40_m5_prior_fire_tape.csv", prior)
    write_csv(OUT / "de40_m5_tip_core_fire_tape.csv", tip_core)
    if tip:
        write_csv(OUT / "de40_m5_tip_fire_tape.csv", tip)
        write_csv(OUT / "de40_m5_tip_prior_fire_tape.csv", tip + prior)
    if sep_oct:
        write_csv(OUT / "de40_m5_sep_oct_fire_tape.csv", sep_oct)

    ASSETS_TAPES.mkdir(parents=True, exist_ok=True)
    write_csv(ASSETS_TAPES / "de40_m5_ytd_fire_tape_v0.csv", long)
    write_csv(ASSETS_TAPES / "de40_m5_prior_fire_tape_v0.csv", prior)
    write_csv(ASSETS_TAPES / "de40_m5_tip_core_fire_tape_v0.csv", tip_core)
    if tip:
        write_csv(ASSETS_TAPES / "de40_m5_tip_fire_tape_v0.csv", tip)
        write_csv(ASSETS_TAPES / "de40_m5_tip_prior_fire_tape_v0.csv", tip + prior)
    if sep_oct:
        write_csv(ASSETS_TAPES / "de40_m5_sep_oct_fire_tape_v0.csv", sep_oct)

    cost_rows = tip if tip else tip_core
    cost_win = cost_rows[0]["window"] if cost_rows else "unknown"
    cost = cost_proxy(cost_rows, cost_win)
    (OUT / "COST_PROXY.json").write_text(
        json.dumps(cost, indent=2), encoding="utf-8"
    )

    profiles: dict = {
        "task": "DE40-M5-AOS-P1",
        "log": str(log_path),
        "ytd": profile_slices(long, "ytd"),
        "prior": profile_slices(prior, "prior") if prior else {"n": 0},
        "tip_core": profile_slices(tip_core, "tip_core") if tip_core else {"n": 0},
        "sep_oct": profile_slices(sep_oct, "sep_oct") if sep_oct else {"n": 0},
        "cost_proxy": cost,
    }
    if tip:
        profiles["tip"] = profile_slices(tip, "tip")
    (OUT / "TAPE_QA.json").write_text(
        json.dumps(profiles, indent=2), encoding="utf-8"
    )
    summary = {k: profiles[k] for k in profiles if k not in ("cost_proxy", "log")}
    print(json.dumps(summary, indent=2))
    print(json.dumps(cost, indent=2))
    print(
        f"ytd={len(long)} prior={len(prior)} tip_core={len(tip_core)} "
        f"tip={len(tip) if tip else 0} sep_oct={len(sep_oct)}"
    )


if __name__ == "__main__":
    main()
