//+------------------------------------------------------------------+
//| AOS_L2det_uk_m5.mqh — UK100 M5 deterministic L2 skip map v1b      |
//| Policy: doc/assets/UK100/aos_l2_policy_M5.md                      |
//| Stack: (Mon ∧ hour∈{12,13}) ∨ (SELL ∧ hour∈{12,13})               |
//| Optional: Aug calendar seed (tip-only; off by default)           |
//| Do NOT use on M15 — M15 map remains AOS_L2det_uk.mqh              |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_UK_M5_MQH
#define AOS_L2DET_UK_M5_MQH

#define AOS_L2DET_UK_M5_SEMVER "L2det_uk_m5_v1b_20261020"

//+------------------------------------------------------------------+
// Returns true if M5 L2det wants to withhold. reason set when true.
// Caller must gate on UK100 + PERIOD_M5.
bool AOSUkM5L2detShouldSkip(const ENUM_BMRG_SIDE side,
                            const datetime t,
                            string &reason)
  {
   reason = "";
   if(!InpAOS_UK_M5_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   // dt.day_of_week: 0=Sun · 1=Mon · … · 6=Sat
   const bool isMon = (dt.day_of_week == 1);
   const bool isH12_13 = (dt.hour == 12 || dt.hour == 13);
   const bool isSell = (side == BMRG_SIDE_SELL);

   string parts = "";

   if(InpAOS_UK_M5_SkipMonAndH12 && isMon && isH12_13)
      parts = "L2DET_SKIP_MON_AND_H12";

   if(InpAOS_UK_M5_SkipSellAndH12 && isSell && isH12_13)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_SELL_AND_H12";
     }

   // Optional tip calendar seed — keep OFF for multi-year / live
   if(InpAOS_UK_M5_SkipAug && dt.mon == 8)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_AUG";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_UK_M5_MQH
