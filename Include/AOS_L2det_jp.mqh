//+------------------------------------------------------------------+
//| AOS_L2det_jp.mqh — JP225/JPN225 M15 deterministic L2 skip map v1 |
//| Policy: doc/assets/JP225/aos_l2_policy.md                         |
//| Armed: month==May OR month==Jul (all sides)                       |
//| Gate: InpAOS_JP_L2detEnable — research OS / JPN225stack only      |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_JP_MQH
#define AOS_L2DET_JP_MQH

#define AOS_L2DET_JP_SEMVER "L2det_jp225_v1_May_OR_Jul_20261019"

//+------------------------------------------------------------------+
bool AOSIsJp225Symbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   if(StringFind(s, "JPN225") >= 0)
      return true;
   if(StringFind(s, "JP225") >= 0)
      return true;
   if(StringFind(s, "NI225") >= 0)
      return true;
   if(StringFind(s, "NIKKEI") >= 0)
      return true;
   if(StringFind(s, "NKY") >= 0)
      return true;
   return false;
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSJpL2detShouldSkip(const ENUM_BMRG_SIDE side,
                          const datetime t,
                          string &reason)
  {
   reason = "";
   if(!InpAOS_JP_L2detEnable)
      return false;
   if(!AOSIsJp225Symbol())
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   string parts = "";

   // Primary ARM: May ∨ Jul (P2 · P6 keep — never Wed LIVE)
   if(InpAOS_JP_SkipMay && dt.mon == 5)
      parts = "L2DET_SKIP_MAY";

   if(InpAOS_JP_SkipJul && dt.mon == 7)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_JUL";
     }

   // Optional HOLD challenger (off by default — Aug FP)
   if(InpAOS_JP_SkipWed && dt.day_of_week == 3)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_WED";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_JP_MQH
