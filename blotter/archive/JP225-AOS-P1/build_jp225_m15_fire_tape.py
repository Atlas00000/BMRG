"""JP225/JPN225 M15: labeled fire tapes (tip + Jan–Aug + long) + journal Leak proxy."""
from __future__ import annotations

import csv
import json
import re
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
    r"\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\BMRG\doc\assets\JP225\tapes"
)

SL_PTS = 23260.0
ATR_MAX = 19670.0
R_DESIGN = 1.50
BWR = 1.0 / (1.0 + R_DESIGN)
LEAK_PRIOR = 0.043  # ~4.3 pp
MAGIC = "26101904"
PRESET = "BMRG-M15-JP225-6M-P1_wrLift_fade_chart"
# tip Δ$9.28 / net ~6R → ~1.547 $/R (label-time proxy only)
R_CCY = 1.5467

WINDOWS = {
    "tip": {
        "id": "2026.05.01-2026.08.31",
        "expect_n": 79,
        "from": "2026.05.01",
        "to": "2026.08.31",
    },
    "janaug": {
        "id": "2026.01.01-2026.08.31",
        "expect_n": 143,
        "from": "2026.01.01",
        "to": "2026.08.31",
    },
    "long": {
        "id": "2025.01.01-2026.10.18",
        "expect_n": 360,
        "from": "2025.01.01",
        "to": "2026.10.18",
    },
}

# Ouroboros H1 meanrev tags (known tip months + long footnotes)
OURO = {
    "2026-05": "FRAGILE",
    "2026-06": "FRAGILE",
    "2026-07": "MISMATCH",
    "2026-08": "MATCH",
    "2026-09": "MATCH",
    "2026-10": "MISMATCH",
}

START_RE = re.compile(
    r"JPN225,M15: testing of Experts\\BMRG\\BMRG\.ex5 "
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
        tp = text.find("Test passed", s.end())
        if tp != -1 and tp < end:
            end = tp + len("Test passed")
        chunk = text[s.start() : end]
        mag = re.search(r"InpMagic=(\d+)", chunk[:12000])
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
            win = kind == "TP"
            pnl_r = R_DESIGN if win else -1.0
            month = od.strftime("%Y-%m")
            atr = open_t["atr_pts"]
            tag = OURO.get(month, "")
            near = int(atr is not None and atr >= 0.9 * ATR_MAX)
            session_age = max(0, (od.hour - 8) * 60 + od.minute)
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
                    "session_age_min": session_age,
                    "ouroboros_tag": tag,
                    "nights_held": int(hold_h >= 12),
                    "near_atr_cap": near,
                    "cell_month_may": int(od.month == 5),
                    "cell_month_jul": int(od.month == 7),
                    "cell_month_oct": int(od.month == 10),
                    "cell_mismatch": int(tag == "MISMATCH"),
                    "cell_fragile": int(tag == "FRAGILE"),
                    "cell_may_fragile": int(od.month == 5 and tag == "FRAGILE"),
                    "cell_near_atr": near,
                    "magic": int(MAGIC),
                    "symbol": "JPN225",
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
        "task": "JP225-AOS-P1",
        "window": "2026.05.01-2026.08.31",
        "magic": int(MAGIC),
        "symbol": "JPN225",
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
        "Leak_prior_pp": round(LEAK_PRIOR * 100, 4),
        "EF_prior_pp": round((bm - LEAK_PRIOR) * 100, 4),
        "Leak_source": "journal_2x_entry_spread_median",
        "note": (
            "Not full deal blotter (no exit spread/commission/swap). "
            "Tester entry spreads may understate live ~2300 pts — "
            "replace with measured deals when exported. "
            "Prior ~4.3 pp remains Stage-1 authority until then."
        ),
        "zone": "regime_fragile_tip_prior",
    }


def slice_stats(subset: list[dict]) -> dict:
    if not subset:
        return {"n": 0}
    n = len(subset)
    wr = sum(r["win"] for r in subset) / n
    en = sum(r["pnl_R_design"] for r in subset) / n
    return {"n": n, "WR": round(wr, 4), "E_N": round(en, 4)}


def profile_slices(rows: list[dict], title: str) -> dict:
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
    by_tag = {
        t: slice_stats([r for r in rows if r["ouroboros_tag"] == t])
        for t in ("MATCH", "MISMATCH", "FRAGILE", "")
    }
    return {
        "title": title,
        "n": len(rows),
        "by_side": by_side,
        "by_dow": by_dow,
        "by_hour": by_hour,
        "by_month": by_month,
        "by_ouroboros": by_tag,
        "near_atr_cap": slice_stats([r for r in rows if r["near_atr_cap"] == 1]),
        "cell_may_fragile": slice_stats(
            [r for r in rows if r["cell_may_fragile"] == 1]
        ),
        "nights_held_share": round(
            sum(r["nights_held"] for r in rows) / len(rows), 4
        ),
        "med_hold_h_win": round(
            median([r["hold_h"] for r in rows if r["win"] == 1] or [0]), 4
        ),
        "med_hold_h_lose": round(
            median([r["hold_h"] for r in rows if r["win"] == 0] or [0]), 4
        ),
        "atr_missing_n": sum(1 for r in rows if r["atr_pts"] is None),
    }


def dedupe_combined(a: list[dict], b: list[dict]) -> list[dict]:
    keys = {(r["open_time"], r["side"]) for r in a}
    out = list(a)
    for r in b:
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
        write_csv(OUT / f"jp225_{name}_fire_tape.csv", rows)
        write_csv(ASSETS_TAPES / f"jp225_{name}_fire_tape_v0.csv", rows)
        print(f"{name}: n={len(rows)}")

    combined = dedupe_combined(by_name["tip"], by_name["janaug"])
    write_csv(OUT / "jp225_tip_janaug_fire_tape.csv", combined)
    write_csv(ASSETS_TAPES / "jp225_tip_janaug_fire_tape_v0.csv", combined)

    cost = tip_cost(by_name["tip"])
    (OUT / "COST_PROXY.json").write_text(
        json.dumps(cost, indent=2), encoding="utf-8"
    )
    print(json.dumps(cost, indent=2))

    profiles = {
        "tip": profile_slices(by_name["tip"], "tip"),
        "janaug": profile_slices(by_name["janaug"], "janaug"),
        "long": profile_slices(by_name["long"], "long"),
    }
    (OUT / "TAPE_QA.json").write_text(
        json.dumps(profiles, indent=2), encoding="utf-8"
    )
    print(f"combined tip+janaug n={len(combined)}")
    print("tip side", profiles["tip"]["by_side"])
    print("tip dow", {k: v for k, v in profiles["tip"]["by_dow"].items() if v.get("n")})
    print("tip ouro", profiles["tip"]["by_ouroboros"])


if __name__ == "__main__":
    main()
