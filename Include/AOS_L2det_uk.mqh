//+------------------------------------------------------------------+
//| AOS_L2det_uk.mqh — UK100 deterministic L2 skip map v1b             |
//| Policy: doc/assets/UK100/aos_l2_policy.md                          |
//| Stack: Thu OR (BUY ∧ atrPts >= nearFrac × atrCap)                  |
//| Optional: Jul calendar seed (tip-only; off by default)             |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_UK_MQH
#define AOS_L2DET_UK_MQH

#include "Indicators.mqh"

#define AOS_L2DET_UK_SEMVER "L2det_uk_v1b_20261012"

//+------------------------------------------------------------------+
bool AOSIsUk100Symbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   if(StringFind(s, "UK100") >= 0)
      return true;
   if(StringFind(s, "FTSE") >= 0)
      return true;
   if(StringFind(s, "UKX") >= 0)
      return true;
   return false;
  }

//+------------------------------------------------------------------+
double AOSUkCurrentAtrPoints()
  {
   BandValues bands;
   if(!IndicatorsRead(1, bands))
      return 0.0;
   return IndicatorsATRPoints(bands);
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSUkL2detShouldSkip(const ENUM_BMRG_SIDE side,
                          const datetime t,
                          string &reason)
  {
   reason = "";
   if(!InpAOS_UK_L2detEnable)
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   string parts = "";

   // dt.day_of_week: 0=Sun … 4=Thu … 6=Sat
   if(InpAOS_UK_SkipThu && dt.day_of_week == 4)
      parts = "L2DET_SKIP_THU";

   if(InpAOS_UK_SkipBuyNearAtr && side == BMRG_SIDE_BUY)
     {
      const double atrPts = AOSUkCurrentAtrPoints();
      const double thr = InpAOS_UK_NearAtrFrac * InpAOS_UK_AtrCapPoints;
      if(atrPts > 0.0 && atrPts >= thr)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_SKIP_BUY_NEAR_ATR";
        }
     }

   // Optional tip calendar seed — keep OFF for multi-year / live
   if(InpAOS_UK_SkipJul && dt.mon == 7)
     {
      if(StringLen(parts) > 0)
         parts += "|";
      parts += "L2DET_SKIP_JUL";
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_UK_MQH
