//+------------------------------------------------------------------+
//| Filters.mqh — time + regime gates                                  |
//+------------------------------------------------------------------+
#ifndef BMRG_FILTERS_MQH
#define BMRG_FILTERS_MQH

#include "Config.mqh"
#include "Indicators.mqh"
#include "Logger.mqh"

//+------------------------------------------------------------------+
bool FiltersWeekdayAllowed(const datetime t)
  {
   MqlDateTime dt;
   TimeToStruct(t, dt);
   switch(dt.day_of_week)
     {
      case 0: return InpTradeSun;
      case 1: return InpTradeMon;
      case 2: return InpTradeTue;
      case 3: return InpTradeWed;
      case 4: return InpTradeThu;
      case 5: return InpTradeFri;
      case 6: return InpTradeSat;
     }
   return false;
  }

//+------------------------------------------------------------------+
bool FiltersInSession(const datetime t)
  {
   if(!InpUseTimeFilter)
      return true;

   MqlDateTime dt;
   TimeToStruct(t, dt);
   const int nowMin = dt.hour * 60 + dt.min;
   const int startMin = InpStartHour * 60 + InpStartMinute;
   const int endMin   = InpEndHour * 60 + InpEndMinute;

   if(startMin == endMin)
      return true; // 24h

   if(startMin < endMin)
      return (nowMin >= startMin && nowMin < endMin);

   // Overnight window (e.g. 22:00–06:00)
   return (nowMin >= startMin || nowMin < endMin);
  }

//+------------------------------------------------------------------+
bool FiltersTimeOk(string &reason)
  {
   reason = "";
   const datetime now = TimeCurrent();

   if(!FiltersWeekdayAllowed(now))
     {
      reason = "weekday blocked";
      return false;
     }
   if(!FiltersInSession(now))
     {
      reason = "outside session";
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
bool FiltersRegimeOk(const BandValues &bands, string &reason)
  {
   reason = "";
   if(!bands.valid)
     {
      reason = "bands invalid";
      return false;
     }

   if(InpUseATRRegime)
     {
      const double atrPts = IndicatorsATRPoints(bands);
      if(InpATRMinPoints > 0.0 && atrPts < InpATRMinPoints)
        {
         reason = StringFormat("ATR %.1f < min %.1f pts", atrPts, InpATRMinPoints);
         return false;
        }
      if(InpATRMaxPoints > 0.0 && atrPts > InpATRMaxPoints)
        {
         reason = StringFormat("ATR %.1f > max %.1f pts", atrPts, InpATRMaxPoints);
         return false;
        }
     }

   if(InpUseBBWidthRegime)
     {
      if(InpBBWidthMinPct > 0.0 && bands.bbWidthPct < InpBBWidthMinPct)
        {
         reason = StringFormat("BB width %.2f%% < min %.2f%%", bands.bbWidthPct, InpBBWidthMinPct);
         return false;
        }
      if(InpBBWidthMaxPct > 0.0 && bands.bbWidthPct > InpBBWidthMaxPct)
        {
         reason = StringFormat("BB width %.2f%% > max %.2f%%", bands.bbWidthPct, InpBBWidthMaxPct);
         return false;
        }
     }

   return true;
  }

//+------------------------------------------------------------------+
bool FiltersAllowEntry(const BandValues &bands, string &reason)
  {
   if(!FiltersTimeOk(reason))
      return false;
   if(!FiltersRegimeOk(bands, reason))
      return false;
   return true;
  }

#endif // BMRG_FILTERS_MQH
