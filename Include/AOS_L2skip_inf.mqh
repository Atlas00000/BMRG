// Auto-generated from L2skip_inf_p92_20260927_223519 — regenerate via infra/src/train/export_l2_mqh.py
#ifndef AOS_L2SKIP_INF_MQH
#define AOS_L2SKIP_INF_MQH

// INF LIVE_WITHHOLD model (sklearn LogisticRegression + OHE + StandardScaler)
// Feature order after pre:
// 0-1  session LON_NY, NY
// 2-3  side BUY, SELL
// 4-7  dow Fri, Mon, Thu, Wed
// 8-15 scaled numerics: hour, spread, month, wom, is_mon, is_fri, side_buy, spread_hi

#define AOS_L2INF_SEMVER      "L2skip_inf_p92_20260927_223519"
#define AOS_L2INF_THR         0.5761284981
#define AOS_L2INF_UNCERTAIN   0.03
#define AOS_L2INF_INTERCEPT   -0.0127389095
#define AOS_L2INF_N_FEAT      16
#define AOS_L2INF_SPREAD_MED  6.0

const double AOS_L2INF_COEF[AOS_L2INF_N_FEAT] =
  {
    0.0324841372, -0.0428968683, -0.0089619545, -0.0014507766,
   -0.0239938683, -0.0104442551,  0.0058568245,  0.0181685677,
    0.0777826792, -0.1195008926,  0.1515953197,  0.1239043813,
   -0.0192191452, -0.0503656608, -0.0077489242,  0.1715089275
  };

// StandardScaler mean / scale for NUM features (same order as 8..15)
const double AOS_L2INF_NUM_MEAN[8] =
  {
   14.2641509434, 5.5018867925, 5.3490566038, 2.7471698113,
    0.2283018868, 0.2396226415, 0.4886792453, 0.5528301887
  };

const double AOS_L2INF_NUM_SCALE[8] =
  {
    2.2474383186, 2.9609082343, 3.0295477364, 1.2798295543,
    0.4197381747, 0.4268531729, 0.4998718241, 0.4972011375
  };

#endif // AOS_L2SKIP_INF_MQH
