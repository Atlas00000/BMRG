//+------------------------------------------------------------------+
//| AOS_L2det_usdjpy.mqh — USDJPY M15 deterministic L2 skip map v1c   |
//| Policy: doc/assets/USDJPY/aos_l2_policy.md                         |
//| Armed: near_atr (atr >= frac×cap) OR hour==16                      |
//| Gate: InpAOS_USDJPY_L2detEnable — research OS / USDJPYstack only   |
//+------------------------------------------------------------------+
#ifndef AOS_L2DET_USDJPY_MQH
#define AOS_L2DET_USDJPY_MQH

#include "Indicators.mqh"

#define AOS_L2DET_USDJPY_SEMVER "L2det_usdjpy_v1c_near_atr_OR_H16_20261019"

//+------------------------------------------------------------------+
bool AOSIsUsdJpySymbol()
  {
   string s = _Symbol;
   StringToUpper(s);
   if(StringFind(s, "USDJPY") >= 0)
      return true;
   return false;
  }

//+------------------------------------------------------------------+
double AOSUsdJpyCurrentAtrPoints()
  {
   BandValues bands;
   if(!IndicatorsRead(1, bands))
      return 0.0;
   return IndicatorsATRPoints(bands);
  }

//+------------------------------------------------------------------+
// Returns true if L2det wants to withhold. reason set when true.
bool AOSUsdJpyL2detShouldSkip(const ENUM_BMRG_SIDE side,
                              const datetime t,
                              string &reason)
  {
   reason = "";
   if(!InpAOS_USDJPY_L2detEnable)
      return false;
   if(!AOSIsUsdJpySymbol())
      return false;

   string parts = "";

   // Primary ARM v1c: near ATR cap (P2/P6 keep 0.9×70)
   if(InpAOS_USDJPY_SkipNearAtr)
     {
      const double atrPts = AOSUsdJpyCurrentAtrPoints();
      const double thr = InpAOS_USDJPY_NearAtrFrac * InpAOS_USDJPY_AtrCapPoints;
      if(atrPts > 0.0 && atrPts >= thr)
         parts = "L2DET_SKIP_NEAR_ATR";
     }

   // Primary ARM v1c: hour==16
   if(InpAOS_USDJPY_SkipH16)
     {
      MqlDateTime dt;
      TimeToStruct(t, dt);
      if(dt.hour == 16)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_SKIP_H16";
        }
     }

   // Optional HOLD challenger (off by default — protect FP)
   if(InpAOS_USDJPY_SkipJul)
     {
      MqlDateTime dt;
      TimeToStruct(t, dt);
      if(dt.mon == 7)
        {
         if(StringLen(parts) > 0)
            parts += "|";
         parts += "L2DET_SKIP_JUL_HOLD";
        }
     }

   if(StringLen(parts) == 0)
      return false;

   reason = parts;
   return true;
  }

#endif // AOS_L2DET_USDJPY_MQH
