//+------------------------------------------------------------------+
//| AOS_L2det_aud.mqh — AUDUSD M15 deterministic L2 skip map v1        |
//| Policy: doc/assets/AUDUSD/aos_l2_policy.md                         |
//| Stack: BUY ∧ month==May                                           |
//| Gate: InpAOS_AUD_L2detEnable — do NOT arm on live M5 SCALE 8230931|
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_AUD_MQH
#define AOS_L2DET_AUD_MQH

#define AOS_L2DET_AUD_SEMVER "L2det_aud_m15_v1_20261019"

//+------------------------------------------------------------------+
bool AOSIsAudUsdSymbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   return (StringFind(s, "AUDUSD") == 0);
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSAudL2detShouldSkip(const ENUM_BMRG_SIDE side,
                           const datetime t,
                           string &reason)
  {
   reason = "";
   if(!InpAOS_AUD_L2detEnable)
      return false;
   if(!AOSIsAudUsdSymbol())
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   string parts = "";

   // Preferred atom: BUY ∧ May (dt.mon is 1..12)
   if(InpAOS_AUD_SkipBuyMay && side == BMRG_SIDE_BUY && dt.mon == 5)
      parts = "L2DET_SKIP_BUY_MAY";

   // Optional alt atom (default off) — BUY ∧ Thu
   if(InpAOS_AUD_SkipBuyThu && side == BMRG_SIDE_BUY && dt.day_of_week == 4)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_BUY_THU";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_AUD_MQH
