//+------------------------------------------------------------------+
//| AOS_L2det_de_m5.mqh — DE40/DE30 M5 deterministic L2 skip map v1b |
//| Policy: doc/assets/DE40/aos_l2_policy_M5.md                       |
//| Stack: (BUY ∧ hour∈{14,16}) ∨ (BUY ∧ month==Oct)                 |
//| Do NOT use on M15 — M15 map remains AOS_L2det_de.mqh             |
//| Never blanket-skip near_atr on M5 (tip near_atr is a star)       |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_DE_M5_MQH
#define AOS_L2DET_DE_M5_MQH

#define AOS_L2DET_DE_M5_SEMVER "L2det_de40_m5_v1b_20261020"

//+------------------------------------------------------------------+
// Returns true if M5 L2det wants to withhold. reason set when true.
// Caller must gate on DE40/DE30 + PERIOD_M5.
bool AOSDeM5L2detShouldSkip(const ENUM_BMRG_SIDE side,
                            const datetime t,
                            string &reason)
  {
   reason = "";
   if(!InpAOS_DE_M5_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   const bool isBuy = (side == BMRG_SIDE_BUY);
   const bool isH14_16 = (dt.hour == 14 || dt.hour == 16);
   const bool isOct = (dt.mon == 10);

   string parts = "";

   // Primary ARM v1b: BUY ∧ late session
   if(InpAOS_DE_M5_SkipBuyH14_16 && isBuy && isH14_16)
      parts = "L2DET_SKIP_BUY_H14_16";

   // Primary ARM v1b: BUY ∧ October FRAGILE
   if(InpAOS_DE_M5_SkipBuyOct && isBuy && isOct)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_BUY_OCT";
     }

   // Optional aggressive (SELL collateral) — OFF by default
   if(InpAOS_DE_M5_SkipH14_16All && isH14_16)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_H14_16";
     }

   // Optional Oct all sides — OFF by default (1 SELL FP on tip)
   if(InpAOS_DE_M5_SkipOctAll && isOct)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_OCT";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_DE_M5_MQH
