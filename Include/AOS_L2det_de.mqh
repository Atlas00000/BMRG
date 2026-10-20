//+------------------------------------------------------------------+
//| AOS_L2det_de.mqh — DE40/DE30 M15 deterministic L2 skip map v1     |
//| Policy: doc/assets/DE40/aos_l2_policy.md                           |
//| Armed: BUY ∧ atrPts >= nearFrac × atrCap (default 0.9×4070)       |
//| Gate: InpAOS_DE_L2detEnable — research OS / DE40stack only         |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_DE_MQH
#define AOS_L2DET_DE_MQH

#include "Indicators.mqh"

#define AOS_L2DET_DE_SEMVER "L2det_de40_v1_BUY_near_atr_20261019"

//+------------------------------------------------------------------+
bool AOSIsDe40Symbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   if(StringFind(s, "DE30") >= 0)
      return true;
   if(StringFind(s, "DE40") >= 0)
      return true;
   if(StringFind(s, "GER40") >= 0)
      return true;
   if(StringFind(s, "GER30") >= 0)
      return true;
   if(StringFind(s, "GDAXI") >= 0)
      return true;
   // bare DAX — avoid matching unrelated symbols with "DAX" mid-token when possible
   if(StringFind(s, "DAX") >= 0)
      return true;
   return false;
  }

//+------------------------------------------------------------------+
double AOSDeCurrentAtrPoints()
  {
   BandValues bands;
   if(!IndicatorsRead(1, bands))
      return 0.0;
   return IndicatorsATRPoints(bands);
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSDeL2detShouldSkip(const ENUM_BMRG_SIDE side,
                          const datetime t,
                          string &reason)
  {
   reason = "";
   if(!InpAOS_DE_L2detEnable)
      return false;
   if(!AOSIsDe40Symbol())
      return false;

   string parts = "";

   // Primary ARM: BUY ∧ near ATR cap (P2 · P6 keep 0.9×4070)
   if(InpAOS_DE_SkipBuyNearAtr && side == BMRG_SIDE_BUY)
     {
      const double atrPts = AOSDeCurrentAtrPoints();
      const double thr = InpAOS_DE_NearAtrFrac * InpAOS_DE_AtrCapPoints;
      if(atrPts > 0.0 && atrPts >= thr)
         parts = "L2DET_SKIP_BUY_NEAR_ATR";
     }

   // Optional HOLD challenger (off by default — Aug FP on tip)
   if(InpAOS_DE_SkipH13)
     {
      MqlDateTime dt;
      TimeToStruct(t, dt);
      if(dt.hour == 13)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_SKIP_H13";
        }
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_DE_MQH
