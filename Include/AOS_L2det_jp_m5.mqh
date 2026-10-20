//+------------------------------------------------------------------+
//| AOS_L2det_jp_m5.mqh — JP225/JPN225 M5 deterministic L2 skip v1c  |
//| Policy: doc/assets/JP225/aos_l2_policy_M5.md                      |
//| Stack: (BUY ∧ MATCH) ∨ (BUY ∧ hour∈{9,13,16})                    |
//| MATCH months on tip map: Aug / Sep (mon 8 / 9)                    |
//| Do NOT use on M15 — M15 map remains AOS_L2det_jp.mqh (May∨Jul)   |
//| Never blanket-skip MISMATCH/FRAGILE/near_atr (OFFHOME home on M5)|
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_JP_M5_MQH
#define AOS_L2DET_JP_M5_MQH

#define AOS_L2DET_JP_M5_SEMVER "L2det_jp225_m5_v1c_20261020"

//+------------------------------------------------------------------+
// Returns true if M5 L2det wants to withhold. reason set when true.
// Caller must gate on JP225/JPN225 + PERIOD_M5.
bool AOSJpM5L2detShouldSkip(const ENUM_BMRG_SIDE side,
                            const datetime t,
                            string &reason)
  {
   reason = "";
   if(!InpAOS_JP_M5_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   const bool isBuy = (side == BMRG_SIDE_BUY);
   // Tip MATCH tax months (Ouroboros Aug–Sep)
   const bool isMatchMonth = (dt.mon == 8 || dt.mon == 9);
   const bool isSoftHour = (dt.hour == 9 || dt.hour == 13 || dt.hour == 16);

   string parts = "";

   // Primary ARM v1c: BUY ∧ MATCH (Aug/Sep)
   if(InpAOS_JP_M5_SkipBuyMatch && isBuy && isMatchMonth)
      parts = "L2DET_SKIP_BUY_MATCH";

   // Primary ARM v1c: BUY ∧ soft hours
   if(InpAOS_JP_M5_SkipBuyH09_13_16 && isBuy && isSoftHour)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_BUY_H09_13_16";
     }

   // Optional aggressive MATCH all sides — OFF by default (SELL FP)
   if(InpAOS_JP_M5_SkipMatchAll && isMatchMonth)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_MATCH";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_JP_M5_MQH
