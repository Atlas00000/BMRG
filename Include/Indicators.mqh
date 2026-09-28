//+------------------------------------------------------------------+
//| Indicators.mqh — BB + ATR                                          |
//+------------------------------------------------------------------+
#ifndef BMRG_INDICATORS_MQH
#define BMRG_INDICATORS_MQH

#include "Config.mqh"
#include "Logger.mqh"

int g_bbHandle  = INVALID_HANDLE;
int g_atrHandle = INVALID_HANDLE;

struct BandValues
  {
   double upper;
   double mid;
   double lower;
   double close;
   double atr;
   double bbWidthPct;
   bool   valid;
  };

//+------------------------------------------------------------------+
bool IndicatorsInit()
  {
   g_bbHandle = iBands(_Symbol, _Period, InpBBPeriod, 0, InpBBDev, PRICE_CLOSE);
   if(g_bbHandle == INVALID_HANDLE)
     {
      LogError("iBands create failed, err=" + IntegerToString(GetLastError()));
      return false;
     }

   g_atrHandle = iATR(_Symbol, _Period, InpATRPeriod);
   if(g_atrHandle == INVALID_HANDLE)
     {
      LogError("iATR create failed, err=" + IntegerToString(GetLastError()));
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
void IndicatorsRelease()
  {
   if(g_bbHandle != INVALID_HANDLE)
     {
      IndicatorRelease(g_bbHandle);
      g_bbHandle = INVALID_HANDLE;
     }
   if(g_atrHandle != INVALID_HANDLE)
     {
      IndicatorRelease(g_atrHandle);
      g_atrHandle = INVALID_HANDLE;
     }
  }

//+------------------------------------------------------------------+
bool IndicatorsRead(const int shift, BandValues &out)
  {
   out.valid = false;
   out.upper = out.mid = out.lower = out.close = out.atr = out.bbWidthPct = 0.0;

   if(g_bbHandle == INVALID_HANDLE || g_atrHandle == INVALID_HANDLE)
      return false;

   double upper[], mid[], lower[], atr[];
   ArraySetAsSeries(upper, true);
   ArraySetAsSeries(mid, true);
   ArraySetAsSeries(lower, true);
   ArraySetAsSeries(atr, true);

   if(CopyBuffer(g_bbHandle, 1, shift, 1, upper) < 1)
      return false;
   if(CopyBuffer(g_bbHandle, 0, shift, 1, mid) < 1)
      return false;
   if(CopyBuffer(g_bbHandle, 2, shift, 1, lower) < 1)
      return false;
   if(CopyBuffer(g_atrHandle, 0, shift, 1, atr) < 1)
      return false;

   double close[];
   ArraySetAsSeries(close, true);
   if(CopyClose(_Symbol, _Period, shift, 1, close) < 1)
      return false;

   out.upper = upper[0];
   out.mid   = mid[0];
   out.lower = lower[0];
   out.close = close[0];
   out.atr   = atr[0];
   if(out.mid != 0.0)
      out.bbWidthPct = 100.0 * (out.upper - out.lower) / MathAbs(out.mid);
   out.valid = true;
   return true;
  }

//+------------------------------------------------------------------+
bool IndicatorsSigma(const BandValues &bands, double &sigma)
  {
   sigma = 0.0;
   if(!bands.valid || InpBBDev <= 0.0)
      return false;
   sigma = (bands.upper - bands.mid) / InpBBDev;
   return (sigma > 0.0);
  }

//+------------------------------------------------------------------+
double IndicatorsATRPoints(const BandValues &bands)
  {
   const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(point <= 0.0 || !bands.valid)
      return 0.0;
   return bands.atr / point;
  }

#endif // BMRG_INDICATORS_MQH
