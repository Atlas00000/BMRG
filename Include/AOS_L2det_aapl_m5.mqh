//+------------------------------------------------------------------+
//| AOS_L2det_aapl_m5.mqh — Apple M5 deterministic L2 skip map v1b   |
//| Policy: doc/assets/AAPL/aos_l2_policy_M5.md                       |
//| Stack v1b: (month==Jul) ∨ (DOW==Wed)                             |
//| Optional: hour==18 · spread≥thr · H1 Jan–Apr (OFF by default)    |
//| Do NOT use on M15 — M15 map remains AOS_L2det_aapl.mqh (Thu/18)  |
//| Never blanket-skip May / Mon / all BUY                           |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_AAPL_M5_MQH
#define AOS_L2DET_AAPL_M5_MQH

#define AOS_L2DET_AAPL_M5_SEMVER "L2det_aapl_m5_v1b_20261020"

//+------------------------------------------------------------------+
// Returns true if M5 L2det wants to withhold. reason set when true.
// Caller must gate on Apple/AAPL + PERIOD_M5.
bool AOSAppleM5L2detShouldSkip(const datetime t, string &reason)
  {
   reason = "";
   if(!InpAOS_AAPL_M5_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   // dt.day_of_week: 0=Sun … 3=Wed … 6=Sat
   const bool isWed = (dt.day_of_week == 3);
   const bool isJul = (dt.mon == 7);
   const bool isH18 = (dt.hour == 18);
   const bool isH1  = (dt.mon >= 1 && dt.mon <= 4); // Jan–Apr (calendar year)

   string parts = "";

   // Primary ARM v1b: July FRAGILE
   if(InpAOS_AAPL_M5_SkipJul && isJul)
      parts = "L2DET_AAPL_M5_JUL";

   // Primary ARM v1b: Wednesday soft
   if(InpAOS_AAPL_M5_SkipWed && isWed)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_AAPL_M5_WED";
     }

   // Optional HOLD: hour 18 (tip lift OK · 2 May FP — OFF by default)
   if(InpAOS_AAPL_M5_SkipHour18 && isH18)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_AAPL_M5_H18";
     }

   // Optional HOLD: high entry spread (OFF by default)
   if(InpAOS_AAPL_M5_SkipHighSpread)
     {
      const int spr = (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
      if(spr >= InpAOS_AAPL_M5_SpreadThr)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_AAPL_M5_SPREAD";
        }
     }

   // Optional HOLD: H1 Jan–Apr seasonal (tip NO_OP · YTD HOLD — OFF by default)
   if(InpAOS_AAPL_M5_SkipH1 && isH1)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_AAPL_M5_H1";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_AAPL_M5_MQH
