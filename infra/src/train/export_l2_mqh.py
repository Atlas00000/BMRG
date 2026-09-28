"""Export pinned L2 INF model to Include/AOS_L2skip_inf.mqh for EA LIVE_WITHHOLD."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

INFRA = Path(__file__).resolve().parents[2]
BMRG = INFRA.parent
PIN = INFRA / "artefacts" / "models" / "L2skip" / "LATEST_LIVE" / "PIN.json"
OUT = BMRG / "Include" / "AOS_L2skip_inf.mqh"
TAPE = INFRA / "artefacts" / "tape" / "LATEST_REGIME_TAPE.parquet"


def main() -> None:
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    model_dir = Path(pin["path"])
    pipe = joblib.load(model_dir / "model.joblib")
    meta = json.loads((model_dir / "META.json").read_text(encoding="utf-8"))
    pre = pipe.named_steps["pre"]
    clf = pipe.named_steps["clf"]
    ohe = pre.named_transformers_["cat"]
    scaler = pre.named_transformers_["num"]
    tape = pd.read_parquet(TAPE)
    tape = tape[tape["y_lose"].isin([0, 1])]
    spread_med = float(tape["spread_pts"].median())

    coef = clf.coef_[0]
    lines = [
        f"// Auto-generated from {pin['live_semver']} — regenerate via infra/src/train/export_l2_mqh.py",
        "#ifndef AOS_L2SKIP_INF_MQH",
        "#define AOS_L2SKIP_INF_MQH",
        "",
        f'#define AOS_L2INF_SEMVER      "{pin["live_semver"]}"',
        f"#define AOS_L2INF_THR         {float(meta['thr_full_ref']):.10f}",
        f"#define AOS_L2INF_UNCERTAIN   {float(meta.get('uncertain_band', 0.03)):.10f}",
        f"#define AOS_L2INF_INTERCEPT   {float(clf.intercept_[0]):.10f}",
        f"#define AOS_L2INF_N_FEAT      {len(coef)}",
        f"#define AOS_L2INF_SPREAD_MED  {spread_med:.1f}",
        "",
        "const double AOS_L2INF_COEF[AOS_L2INF_N_FEAT] =",
        "  {",
    ]
    # format coefs 4 per line
    for i in range(0, len(coef), 4):
        chunk = ", ".join(f"{c: .10f}" for c in coef[i : i + 4])
        comma = "," if i + 4 < len(coef) else ""
        lines.append(f"   {chunk}{comma}")
    lines += [
        "  };",
        "",
        "const double AOS_L2INF_NUM_MEAN[8] =",
        "  {",
        "   " + ", ".join(f"{v:.10f}" for v in scaler.mean_) + ",",
        "  };",
        "",
        "const double AOS_L2INF_NUM_SCALE[8] =",
        "  {",
        "   " + ", ".join(f"{v:.10f}" for v in scaler.scale_) + ",",
        "  };",
        "",
        f"// OHE cats session={list(ohe.categories_[0])} side={list(ohe.categories_[1])} dow={list(ohe.categories_[2])}",
        "",
        "#endif // AOS_L2SKIP_INF_MQH",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "semver": pin["live_semver"], "n_feat": len(coef)}, indent=2))


if __name__ == "__main__":
    main()
