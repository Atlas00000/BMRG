from pathlib import Path
import struct
from datetime import datetime, timezone

p = Path(
    r"C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal"
    r"\D0E8209F77C8CF37AD8BF550E51FF075\bases\YWO-Trade\history\AUDUSD\cache\M5.hc"
)
raw = p.read_bytes()
print("size", len(raw))
hdr = raw[4:200].decode("utf-16-le", errors="replace")
print("hdr", hdr[:100].encode("ascii", "replace").decode())

for rec in [40, 44, 48, 52, 56, 60, 64, 68, 72, 80]:
    for hoff in (0, 148, 168, 188, 208, 228, 248, 256, 512):
        body = len(raw) - hoff
        if body % rec == 0 and body // rec > 1000:
            print("candidate hoff", hoff, "rec", rec, "n", body // rec)

# brute float layout
hits = 0
for off in range(0, min(len(raw) - 40, 200000), 4):
    t = struct.unpack_from("<I", raw, off)[0]
    if not (1_700_000_000 <= t <= 1_800_000_000):
        continue
    o, h, l, c = struct.unpack_from("<4f", raw, off + 4)
    if 0.55 < o < 0.85 and h >= max(o, c) and l <= min(o, c) and (h - l) < 0.02:
        print("f4", off, datetime.fromtimestamp(t, tz=timezone.utc), o, h, l, c)
        hits += 1
        if hits > 8:
            break
print("float hits", hits)

hits = 0
for off in range(0, min(len(raw) - 48, 200000), 4):
    t = struct.unpack_from("<Q", raw, off)[0]
    if not (1_700_000_000 <= t <= 1_800_000_000):
        continue
    o, h, l, c = struct.unpack_from("<4d", raw, off + 8)
    if 0.55 < o < 0.85 and h >= max(o, c) and l <= min(o, c) and (h - l) < 0.02:
        print("qd", off, datetime.fromtimestamp(t, tz=timezone.utc), o, h, l, c)
        hits += 1
        if hits > 8:
            break
print("qd hits", hits)

# integer price * 100000
hits = 0
for off in range(0, min(len(raw) - 32, 200000), 4):
    t = struct.unpack_from("<I", raw, off)[0]
    if not (1_700_000_000 <= t <= 1_800_000_000):
        continue
    vals = struct.unpack_from("<4i", raw, off + 4)
    o, h, l, c = [v / 100000.0 for v in vals]
    if 0.55 < o < 0.85 and h >= max(o, c) and l <= min(o, c) and (h - l) < 0.02:
        print("i4", off, datetime.fromtimestamp(t, tz=timezone.utc), o, h, l, c)
        hits += 1
        if hits > 8:
            break
print("int hits", hits)
