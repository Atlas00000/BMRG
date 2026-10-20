"""Score JPN225 P0/P1 tester runs from 20261019.log."""
import re
from collections import defaultdict
from pathlib import Path

log = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\Tester\logs\20261019.log"
)

segments = [
    (263612, 298265, "P0_JanAug", 26101903, "2026.01-08"),
    (298398, 315875, "P0_MayAug_tip", 26101903, "2026.05-08"),
    (316008, 320140, "P0_Aug", 26101903, "2026.08"),
    (320273, 329010, "P0_JulAug", 26101903, "2026.07-08"),
    (329154, 337604, "P1_JulAug", 26101904, "2026.07-08"),
    (337736, 371192, "P1_JanAug", 26101904, "2026.01-08"),
    (371325, 388263, "P1_MayAug_tip", 26101904, "2026.05-08"),
    (388399, 478424, "P1_2025_to_tip", 26101904, "2025.01-2026.10"),
]

open_re = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*"
    r"CTrade::OrderSend: market (buy|sell) .*JPN225 "
    r"sl: ([\d.]+) tp: ([\d.]+) \[done at ([\d.]+)\]"
)
tp_re = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*"
    r"take profit triggered #(\d+) (buy|sell) .*JPN225 "
    r"([\d.]+) sl: ([\d.]+) tp: ([\d.]+)"
)
sl_re = re.compile(
    r"(\d{4}\.\d{2}\.\d{2} \d{2}:\d{2}:\d{2}).*"
    r"stop loss triggered #(\d+) (buy|sell) .*JPN225 "
    r"([\d.]+) sl: ([\d.]+) tp: ([\d.]+)"
)

SL_PTS = 23260.0
TP_PTS = 34890.0
POINT = 0.01
c_R = 2500.0 / SL_PTS
R_design = TP_PTS / SL_PTS
leak = c_R / (R_design + 1)

raw = log.read_bytes()[:4]
enc = "utf-8"
if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
    enc = "utf-16"
elif b"\x00" in raw[:200]:
    enc = "utf-16-le"
print("encoding", enc, "size_mb", round(log.stat().st_size / 1e6, 1))

opens, closes = [], []
start_min, end_max = segments[0][0], segments[-1][1]
line_no = 0
with log.open("r", encoding=enc, errors="replace") as f:
    for line in f:
        line_no += 1
        if line_no < start_min:
            continue
        if line_no > end_max:
            break
        if "JPN225" not in line:
            continue
        m = open_re.search(line)
        if m:
            opens.append(
                (
                    line_no,
                    m.group(1),
                    m.group(2),
                    float(m.group(5)),
                    float(m.group(3)),
                    float(m.group(4)),
                )
            )
            continue
        m = tp_re.search(line)
        if m:
            closes.append(
                (
                    line_no,
                    m.group(1),
                    "TP",
                    m.group(3),
                    float(m.group(4)),
                    float(m.group(5)),
                    float(m.group(6)),
                    int(m.group(2)),
                )
            )
            continue
        m = sl_re.search(line)
        if m:
            closes.append(
                (
                    line_no,
                    m.group(1),
                    "SL",
                    m.group(3),
                    float(m.group(4)),
                    float(m.group(5)),
                    float(m.group(6)),
                    int(m.group(2)),
                )
            )

print(f"opens={len(opens)} closes={len(closes)}")


def score(events):
    n = len(events)
    if n == 0:
        return None
    tp = sum(1 for c in events if c[2] == "TP")
    wr = tp / n
    wins, losses = [], []
    for c in events:
        kind, side, entry, slp, tpp = c[2], c[3], c[4], c[5], c[6]
        if side == "buy":
            win_pts = (tpp - entry) / POINT
            loss_pts = (entry - slp) / POINT
        else:
            win_pts = (entry - tpp) / POINT
            loss_pts = (slp - entry) / POINT
        if kind == "TP":
            wins.append(win_pts)
        else:
            losses.append(loss_pts)
    aw = sum(wins) / len(wins) if wins else 0.0
    al = sum(losses) / len(losses) if losses else 1.0
    R = aw / al if al else 0.0
    bwr = 1 / (1 + R) if R > 0 else 0.5
    bm = wr - bwr
    ef = bm - leak
    en = wr * (R + 1) - 1
    return dict(
        n=n, tp=tp, sl=n - tp, wr=wr, R=R, bwr=bwr, bm=bm, leak=leak, ef=ef, en=en
    )


regime = {
    "2026.05": "FRAGILE",
    "2026.06": "FRAGILE",
    "2026.07": "MISMATCH",
    "2026.08": "MATCH",
    "2026.09": "MATCH",
    "2026.10": "MISMATCH",
}

for s, e, label, magic, window in segments:
    cl = [c for c in closes if s <= c[0] <= e]
    op = [o for o in opens if s <= o[0] <= e]
    sc = score(cl)
    print(f"\n=== {label} magic={magic} window={window} ===")
    print(f"  opens={len(op)} closes={len(cl)}")
    if not sc:
        print("  EMPTY")
        continue
    print(
        f"  n={sc['n']} TP={sc['tp']} SL={sc['sl']} "
        f"WR={sc['wr']*100:.1f}% R={sc['R']:.3f} BWR={sc['bwr']*100:.1f}% "
        f"BM={sc['bm']*100:+.1f}pp Leak={sc['leak']*100:.1f}pp "
        f"EF={sc['ef']*100:+.1f}pp E_N={sc['en']:+.3f}R"
    )
    by_m = defaultdict(list)
    for c in cl:
        by_m[c[1][:7]].append(c)
    for m in sorted(by_m):
        scm = score(by_m[m])
        tag = regime.get(m, "?")
        print(
            f"    {m} [{tag:8s}]: n={scm['n']:3d} WR={scm['wr']*100:5.1f}% "
            f"EF={scm['ef']*100:+5.1f}pp E_N={scm['en']:+.3f}R "
            f"TP={scm['tp']}/{scm['n']}"
        )

# MATCH-only vs off-home for P1 tip and long run
print("\n=== Regime slices (P1) ===")
for s, e, label, magic, window in segments:
    if not label.startswith("P1_"):
        continue
    cl = [c for c in closes if s <= c[0] <= e]
    match = [c for c in cl if regime.get(c[1][:7]) == "MATCH"]
    off = [c for c in cl if regime.get(c[1][:7]) in ("FRAGILE", "MISMATCH")]
    for name, subset in (("MATCH", match), ("OFFHOME", off), ("ALL", cl)):
        sc = score(subset)
        if not sc:
            print(f"  {label} {name}: empty")
            continue
        print(
            f"  {label} {name}: n={sc['n']} WR={sc['wr']*100:.1f}% "
            f"EF={sc['ef']*100:+.1f}pp E_N={sc['en']:+.3f}R"
        )

# Geometry integrity P1 tip
print("\n=== Geometry integrity (P1_MayAug_tip) ===")
tips = [o for o in opens if 371325 <= o[0] <= 388263]
tp_lt = 0
dists = []
for o in tips:
    side, entry, sl, tp = o[2], o[3], o[4], o[5]
    if side == "buy":
        slp, tpp = (entry - sl) / POINT, (tp - entry) / POINT
    else:
        slp, tpp = (sl - entry) / POINT, (entry - tp) / POINT
    dists.append((slp, tpp))
    if tpp + 1 < slp:
        tp_lt += 1
if dists:
    sl_mean = sum(d[0] for d in dists) / len(dists)
    tp_mean = sum(d[1] for d in dists) / len(dists)
    print(
        f"opens={len(tips)} mean_SL={sl_mean:.0f} mean_TP={tp_mean:.0f} "
        f"RR={tp_mean/sl_mean:.3f} tp_lt_sl={tp_lt}"
    )
