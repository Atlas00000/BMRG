"""DE40/DE30 M15: labeled fire tapes (tip + YTD) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median

LOG = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)
OUT = Path(__file__).resolve().parent
ASSETS_TAPES = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\DE40\tapes"
)

SL_PTS = 5000.0
ATR_MAX = 4070.0
R_DESIGN = 1.25
BWR = 1.0 / (1.0 + R_DESIGN)
MAGIC = "26101902"
PRESET = "BMRG-M15-DE40-6M-P0_balanced_chart"
# ~$5.81 / 1R @ 0.1 lot from tip AL cluster — label-time proxy only
R_CCY = 5.81

WINDOWS = {
    "tip": {
        "id": "2026.05.01-2026.10.18",
        "expect_n": 77,
        "from": "2026.05.01",
        "to": "2026.10.18",
    },
    "ytd": {
        "id": "2026.01.01-2026.10.18",
        "expect_n": 147,
        "from": "2026.01.01",
        "to": "2026.10.18",
    },
}

# H1 meanrev tags from Ouroboros regime-audit / system_profile
OURO = {
    "2025-06": "MISMATCH",
    "2025-07": "MISMATCH",
    "2025-08": "MATCH",
    "2025-09": "MATCH",
    "2025-10": "MATCH",
    "2025-11": "FRAGILE",
    "2025-12": "MATCH",
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

START_RE = re.compile(
    r"DE30,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
    r"from (\S+) 00:00 to (\S+) 00:00 started with inputs:"
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


def load_text() -> str:
    raw = LOG.read_bytes()
    if raw[:2] == b"\xff\xfe":
        return raw.decode("utf-16-le")
    return raw.decode("utf-8", errors="replace")


def find_chunk(text: str, fro: str, to: str) -> str | None:
    starts = list(START_RE.finditer(text))
    for i, s in enumerate(starts):
        if s.group(1) != fro or s.group(2) != to:
            continue
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        # Prefer end at Test passed inside this span
        tp = text.find("Test passed", s.end())
        if tp != -1 and tp < end:
            end = tp + len("Test passed")
        chunk = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk)
        if mag and mag.group(1) == MAGIC:
            return chunk
    return None


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
            # HALT = daily-loss flatten — treat as loser for avoid-loser labels
            win = kind == "TP"
            # HALT partial R unknown from journal — use −1R design proxy
            pnl_r = R_DESIGN if win else -1.0
            month = od.strftime("%Y-%m")
            atr = open_t["atr_pts"]
            tag = OURO.get(month, "")
            near = int(atr is not None and atr >= 0.9 * ATR_MAX)
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
                    "dow": od.strftime("%a"),
                    "hour": od.hour,
                    "month": month,
                    "ouroboros_tag": tag,
                    "nights_held": int(hold_h >= 12),
                    "near_atr_cap": near,
                    "cell_month_feb": int(month == "2026-02"),
                    "cell_month_mar": int(month == "2026-03"),
                    "cell_mismatch": int(tag == "MISMATCH"),
                    "cell_fragile": int(tag == "FRAGILE"),
                    "cell_near_atr": near,
                    "magic": int(MAGIC),
                    "symbol": "DE30",
                    "preset_id": PRESET,
                    "window": window_id,
                    "tf": "M15",
                }
            )
            open_t = None
            break
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def tip_cost(rows: list[dict]) -> dict:
    spreads = [r["spread_pts"] for r in rows]
    spr_med = float(median(spreads))
    spr_mean = float(mean(spreads))
    c_R = (2.0 * spr_med) / SL_PTS
    leak = c_R / (R_DESIGN + 1.0)
    wr = sum(r["win"] for r in rows) / len(rows)
    bm = wr - BWR
    return {
        "task": "DE40-AOS-P1",
        "window": "2026.05.01-2026.10.18",
        "magic": int(MAGIC),
        "symbol": "DE30",
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
        "SL_pts": SL_PTS,
        "R_design": R_DESIGN,
        "c_R_proxy_2x_med": round(c_R, 6),
        "Leak_proxy_pp": round(leak * 100, 4),
        "EF_proxy_pp": round((bm - leak) * 100, 4),
        "Leak_prior_pp": 9.8,
        "EF_prior_pp": round((bm - 0.098) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Tester entry spreads may understate live ~1020 pts — "
            "replace with measured deals when exported. "
            "Prior 9.8 pp remains Stage-1 authority until then."
        ),
        "zone": "expansion_keep_tip_prior",
    }


def profile_slices(rows: list[dict], title: str) -> dict:
    def slice_stats(subset: list[dict]) -> dict:
        if not subset:
            return {"n": 0}
        n = len(subset)
        wr = sum(r["win"] for r in subset) / n
        en = sum(r["pnl_R_design"] for r in subset) / n
        return {
            "n": n,
            "WR": round(wr, 4),
            "E_N": round(en, 4),
        }

    by_side = {
        s: slice_stats([r for r in rows if r["side"] == s]) for s in ("BUY", "SELL")
    }
    by_dow = {
        d: slice_stats([r for r in rows if r["dow"] == d])
        for d in ("Mon", "Tue", "Wed", "Thu", "Fri")
    }
    by_hour = {}
    hours = sorted({r["hour"] for r in rows})
    for h in hours:
        by_hour[str(h)] = slice_stats([r for r in rows if r["hour"] == h])
    by_month = {}
    for m in sorted({r["month"] for r in rows}):
        by_month[m] = slice_stats([r for r in rows if r["month"] == m])
        by_month[m]["ouroboros_tag"] = OURO.get(m, "")
    near = slice_stats([r for r in rows if r["near_atr_cap"] == 1])
    return {
        "title": title,
        "n": len(rows),
        "by_side": by_side,
        "by_dow": by_dow,
        "by_hour": by_hour,
        "by_month": by_month,
        "near_atr_cap": near,
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 4
        ),
        "med_hold_h_win": round(
            median([r["hold_h"] for r in rows if r["win"] == 1] or [0]), 4
        ),
        "med_hold_h_lose": round(
            median([r["hold_h"] for r in rows if r["win"] == 0] or [0]), 4
        ),
    }


def dedupe_combined(tip: list[dict], ytd: list[dict]) -> list[dict]:
    """Prefer tip rows; append YTD-only opens."""
    keys = {(r["open_time"], r["side"]) for r in tip}
    out = list(tip)
    for r in ytd:
        k = (r["open_time"], r["side"])
        if k not in keys:
            out.append(r)
            keys.add(k)
    out.sort(key=lambda r: r["open_time"])
    return out


def main() -> None:
    text = load_text()
    by_name: dict[str, list[dict]] = {}
    for name, cfg in WINDOWS.items():
        chunk = find_chunk(text, cfg["from"], cfg["to"])
        if chunk is None:
            raise SystemExit(f"missing chunk {name} {cfg['from']}→{cfg['to']}")
        rows = extract(chunk, cfg["id"])
        if len(rows) != cfg["expect_n"]:
            raise SystemExit(
                f"{name}: expected {cfg['expect_n']}, got {len(rows)}"
            )
        by_name[name] = rows
        write_csv(OUT / f"de40_{name}_fire_tape.csv", rows)
        write_csv(ASSETS_TAPES / f"de40_{name}_fire_tape_v0.csv", rows)
        print(f"{name}: n={len(rows)}")

    combined = dedupe_combined(by_name["tip"], by_name["ytd"])
    write_csv(OUT / "de40_tip_ytd_fire_tape.csv", combined)
    write_csv(ASSETS_TAPES / "de40_tip_ytd_fire_tape_v0.csv", combined)

    cost = tip_cost(by_name["tip"])
    (OUT / "COST_PROXY.json").write_text(
        json.dumps(cost, indent=2), encoding="utf-8"
    )
    print(json.dumps(cost, indent=2))

    profiles = {
        "tip": profile_slices(by_name["tip"], "tip"),
        "ytd": profile_slices(by_name["ytd"], "ytd"),
    }
    (OUT / "TAPE_QA.json").write_text(
        json.dumps(profiles, indent=2), encoding="utf-8"
    )
    print(f"combined n={len(combined)}")
    print("tip side", profiles["tip"]["by_side"])
    print("tip dow", {k: v for k, v in profiles["tip"]["by_dow"].items() if v.get("n")})


if __name__ == "__main__":
    main()
