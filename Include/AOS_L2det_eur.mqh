//+------------------------------------------------------------------+
//| AOS_L2det_eur.mqh — EURUSD M15 deterministic L2 skip map v1b       |
//| Policy: doc/assets/EURUSD/aos_l2_policy.md                         |
//| Stack: Thu OR (BUY ∧ atrPts >= nearFrac × atrCap)                  |
//| Gate: InpAOS_EUR_L2detEnable — do NOT arm on M5 Harvest live       |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_EUR_MQH
#define AOS_L2DET_EUR_MQH

#include "Indicators.mqh"

#define AOS_L2DET_EUR_SEMVER "L2det_eur_m15_v1b_20261018"

//+------------------------------------------------------------------+
bool AOSIsEurUsdSymbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   return (StringFind(s, "EURUSD") == 0);
  }

//+------------------------------------------------------------------+
double AOSEurCurrentAtrPoints()
  {
   BandValues bands;
   if(!IndicatorsRead(1, bands))
      return 0.0;
   return IndicatorsATRPoints(bands);
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSEurL2detShouldSkip(const ENUM_BMRG_SIDE side,
                           const datetime t,
                           string &reason)
  {
   reason = "";
   if(!InpAOS_EUR_L2detEnable)
      return false;
   if(!AOSIsEurUsdSymbol())
      return false;

   MqlDateTime dt;
   TimeToStruct(t, dt);

   string parts = "";

   // dt.day_of_week: 0=Sun … 4=Thu … 6=Sat
   if(InpAOS_EUR_SkipThu && dt.day_of_week == 4)
      parts = "L2DET_SKIP_THU";

   if(InpAOS_EUR_SkipBuyNearAtr && side == BMRG_SIDE_BUY)
     {
      const double atrPts = AOSEurCurrentAtrPoints();
      const double thr = InpAOS_EUR_NearAtrFrac * InpAOS_EUR_AtrCapPoints;
      if(atrPts > 0.0 && atrPts >= thr)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_SKIP_BUY_NEAR_ATR";
        }
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_EUR_MQH
