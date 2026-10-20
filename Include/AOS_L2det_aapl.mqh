//+------------------------------------------------------------------+
//| AOS_L2det_aapl.mqh — Apple deterministic L2 skip map v0            |
//| Seeds from doc/assets/AAPL/system_profile.md / aios_roadmap.md     |
//| Cells: DOW_THU · HOUR_18 (server/broker time at decision)          |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_AAPL_MQH
#define AOS_L2DET_AAPL_MQH

#define AOS_L2DET_AAPL_SEMVER "L2det_aapl_v0_20261012"

//+------------------------------------------------------------------+
bool AOSIsAppleSymbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   if(StringFind(s, "APPLE") >= 0)
      return true;
   if(StringFind(s, "AAPL") >= 0)
      return true;
   return false;
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason always set when true.
bool AOSAppleL2detShouldSkip(const datetime t, string &reason)
  {
   reason = "";
   if(!InpAOS_AAPL_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   // dt.day_of_week: 0=Sun … 4=Thu … 6=Sat
   if(InpAOS_AAPL_SkipThu && dt.day_of_week == 4)
     {
      reason = "L2DET_AAPL DOW_THU";
      return true;
     }

   if(InpAOS_AAPL_SkipHour18 && dt.hour == 18)
     {
      reason = "L2DET_AAPL HOUR_18";
      return true;
     }

   return false;
  }

#endif // AOS_L2DET_AAPL_MQH
