// Auto-generated from L2skip_v1 — do not edit by hand
#ifndef AOS_L2SKIP_V1_MQH
#define AOS_L2SKIP_V1_MQH

// Feature order:
// 0-3  dow Fri,Mon,Thu,Wed
// 4-5  session LON_NY,NY
// 6-7  side BUY,SELL
// 8-11 hour_bucket H12_14,H14_16,H16_18,H18_20
// 12   hour
// 13   spread
// 14   month
// 15   week_of_month
// 16   spread_hi
// 17   is_mon
// 18   is_fri
// 19   side_buy

#define AOS_L2_THR       0.57451186
#define AOS_L2_INTERCEPT -1.78357355
#define AOS_L2_N_FEAT    20

const double AOS_L2_COEF[AOS_L2_N_FEAT] =
  {
   -0.06248660, -0.00774055,  0.03547477,  0.03151912,
    0.09439418, -0.09762745, -0.02077628,  0.01754301,
    0.22216487, -0.12777069, -0.02225365, -0.07537380,
    0.10490744, -0.07977800,  0.01961099,  0.09713636,
    0.65682106, -0.00774055, -0.06248660, -0.02077628
  };

#endif // AOS_L2SKIP_V1_MQH
