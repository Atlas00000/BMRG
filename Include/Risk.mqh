//+------------------------------------------------------------------+
//| Risk.mqh — exposure, account %, sizing, containment gates          |
//+------------------------------------------------------------------+
#ifndef BMRG_RISK_MQH
#define BMRG_RISK_MQH

#include "Config.mqh"
#include "State.mqh"
#include "Logger.mqh"
#include "Basket.mqh"
#include "Filters.mqh"
#include "Indicators.mqh"
#include "AOS.mqh"

//+------------------------------------------------------------------+
double RiskAccountBase()
  {
   if(InpRiskBase == BMRG_EQ_BALANCE)
      return AccountInfoDouble(ACCOUNT_BALANCE);
   return AccountInfoDouble(ACCOUNT_EQUITY);
  }

//+------------------------------------------------------------------+
void RiskUpdateEquityHalt()
  {
   if(InpEquityHaltPct <= 0.0)
     {
      g_state.equityHalt = false;
      return;
     }

   const double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   if(g_state.startEquity <= 0.0)
     {
      g_state.startEquity = equity;
      g_state.equityHalt = false;
      return;
     }

   const double ddPct = 100.0 * (g_state.startEquity - equity) / g_state.startEquity;
   if(ddPct >= InpEquityHaltPct)
     {
      if(!g_state.equityHalt)
         LogWarn(StringFormat("Equity halt ON: dd=%.2f%% >= %.2f%%", ddPct, InpEquityHaltPct));
      g_state.equityHalt = true;
     }
  }

//+------------------------------------------------------------------+
void RiskUpdateDailyLossHalt()
  {
   StateRollDayIfNeeded();
   if(InpMaxDailyLossPct <= 0.0)
     {
      g_state.dailyLossHalt = false;
      return;
     }
   if(g_state.dayStartEquity <= 0.0)
      return;

   const double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   const double ddPct = 100.0 * (g_state.dayStartEquity - equity) / g_state.dayStartEquity;
   if(ddPct >= InpMaxDailyLossPct)
     {
      if(!g_state.dailyLossHalt)
         LogWarn(StringFormat("Daily loss halt ON: dd=%.2f%% >= %.2f%%", ddPct, InpMaxDailyLossPct));
      g_state.dailyLossHalt = true;
     }
  }

//+------------------------------------------------------------------+
void RiskTickFailPause()
  {
   if(!g_state.failPause)
      return;
   if(g_state.pauseBarsLeft <= 0)
     {
      g_state.failPause = false;
      g_state.pauseReason = "";
      g_state.consecOrderFails = 0;
      LogInfo("Failure pause cleared");
      return;
     }
   g_state.pauseBarsLeft--;
  }

//+------------------------------------------------------------------+
void RiskTripPause(const string why)
  {
   if(InpFailPauseBars <= 0)
      return;
   g_state.failPause = true;
   g_state.pauseBarsLeft = InpFailPauseBars;
   g_state.pauseReason = why;
   LogWarn(StringFormat("Failure pause %d bars: %s", InpFailPauseBars, why));
  }

//+------------------------------------------------------------------+
void RiskOnOrderFail()
  {
   g_state.consecOrderFails++;
   if(InpMaxOrderFails > 0 && g_state.consecOrderFails >= InpMaxOrderFails)
     {
      RiskTripPause(StringFormat("order fails=%d", g_state.consecOrderFails));
      g_state.consecOrderFails = 0;
     }
  }

//+------------------------------------------------------------------+
void RiskOnOrderSuccess()
  {
   g_state.consecOrderFails = 0;
  }

//+------------------------------------------------------------------+
void RiskOnClosedDealProfit(const double profit)
  {
   if(profit < 0.0)
     {
      g_state.consecLosses++;
      if(InpMaxLossStreak > 0 && g_state.consecLosses >= InpMaxLossStreak)
        {
         RiskTripPause(StringFormat("loss streak=%d", g_state.consecLosses));
         g_state.consecLosses = 0;
        }
     }
   else if(profit > 0.0)
      g_state.consecLosses = 0;
  }

//+------------------------------------------------------------------+
int RiskCurrentSpreadPoints()
  {
   return (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
  }

//+------------------------------------------------------------------+
bool RiskSpreadOk(string &reason)
  {
   reason = "";
   if(InpMaxSpread <= 0)
      return true;
   const int spread = RiskCurrentSpreadPoints();
   if(spread > InpMaxSpread)
     {
      reason = StringFormat("spread %d > max %d", spread, InpMaxSpread);
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
bool RiskCooldownOk(string &reason)
  {
   reason = "";
   if(InpCooldownBars <= 0)
      return true;
   if(g_state.lastEntryBarTime == 0)
      return true;

   const datetime bar0 = iTime(_Symbol, _Period, 0);
   if(bar0 == 0)
     {
      reason = "bar time unavailable";
      return false;
     }

   const int bars = Bars(_Symbol, _Period, g_state.lastEntryBarTime, bar0);
   if(bars > 0 && (bars - 1) < InpCooldownBars)
     {
      reason = StringFormat("cooldown %d/%d bars", bars - 1, InpCooldownBars);
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
double RiskOurMargin()
  {
   double margin = 0.0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !BasketIsOurs(ticket))
         continue;

      const double volume = PositionGetDouble(POSITION_VOLUME);
      const double price  = PositionGetDouble(POSITION_PRICE_CURRENT);
      const long   type   = PositionGetInteger(POSITION_TYPE);
      const ENUM_ORDER_TYPE otype =
         (type == POSITION_TYPE_BUY) ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;

      double need = 0.0;
      if(OrderCalcMargin(otype, _Symbol, volume, price, need))
         margin += need;
     }
   return margin;
  }

//+------------------------------------------------------------------+
double RiskBasketFloatingPnL()
  {
   double pnl = 0.0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !BasketIsOurs(ticket))
         continue;
      pnl += PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP);
     }
   return pnl;
  }

//+------------------------------------------------------------------+
bool RiskExposureOk(string &reason)
  {
   reason = "";
   const double equity = AccountInfoDouble(ACCOUNT_EQUITY);
   if(equity <= 0.0)
     {
      reason = "equity <= 0";
      return false;
     }

   if(InpMaxExposurePct > 0.0)
     {
      const double used = RiskOurMargin();
      const double pct = 100.0 * used / equity;
      if(pct > InpMaxExposurePct)
        {
         reason = StringFormat("exposure %.1f%% > max %.1f%%", pct, InpMaxExposurePct);
         return false;
        }
     }

   if(InpMinFreeMarginPct > 0.0)
     {
      const double free = AccountInfoDouble(ACCOUNT_MARGIN_FREE);
      const double pct = 100.0 * free / equity;
      if(pct < InpMinFreeMarginPct)
        {
         reason = StringFormat("free margin %.1f%% < min %.1f%%", pct, InpMinFreeMarginPct);
         return false;
        }
     }

   if(InpMaxBasketLossPct > 0.0)
     {
      const double pnl = RiskBasketFloatingPnL();
      if(pnl < 0.0)
        {
         const double lossPct = 100.0 * (-pnl) / equity;
         if(lossPct >= InpMaxBasketLossPct)
           {
            reason = StringFormat("basket loss %.2f%% >= max %.2f%%", lossPct, InpMaxBasketLossPct);
            return false;
           }
        }
     }

   return true;
  }

//+------------------------------------------------------------------+
bool RiskDailyOk(string &reason)
  {
   reason = "";
   StateRollDayIfNeeded();
   RiskUpdateDailyLossHalt();

   if(g_state.dailyLossHalt)
     {
      reason = "daily loss halt";
      return false;
     }
   if(InpMaxDailyEntries > 0 && g_state.dailyEntries >= InpMaxDailyEntries)
     {
      reason = StringFormat("daily entries %d >= max %d", g_state.dailyEntries, InpMaxDailyEntries);
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
bool RiskTradeContextOk(string &reason)
  {
   reason = "";
   if(!InpBlockBusyTradeCtx)
      return true;
   if(!TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
     {
      reason = "terminal trade disabled";
      return false;
     }
   if(!MQLInfoInteger(MQL_TRADE_ALLOWED))
     {
      reason = "EA trade disabled";
      return false;
     }
   return true;
  }

//+------------------------------------------------------------------+
bool RiskCanOpenNewEntry(const BandValues &bands, string &reason)
  {
   reason = "";
   StateRollDayIfNeeded();
   RiskUpdateEquityHalt();
   RiskUpdateDailyLossHalt();

   if(g_state.failPause)
     {
      reason = StringFormat("fail pause (%s) barsLeft=%d", g_state.pauseReason, g_state.pauseBarsLeft);
      return false;
     }
   if(g_state.equityHalt)
     {
      reason = "equity halt";
      return false;
     }
   if(!RiskDailyOk(reason))
      return false;
   if(!RiskTradeContextOk(reason))
      return false;
   if(!FiltersAllowEntry(bands, reason))
      return false;

   if(BasketCount() >= InpMaxEntries)
     {
      reason = "max entries reached";
      return false;
     }
   if(g_state.levelsFilled >= InpMaxLevels)
     {
      reason = "max levels reached";
      return false;
     }
   if(!RiskSpreadOk(reason))
      return false;
   if(!RiskCooldownOk(reason))
      return false;
   if(!RiskExposureOk(reason))
      return false;

   // side unknown here — AOSAllowEntry called from ProcessClosedBar with side
   return true;
  }

//+------------------------------------------------------------------+
bool RiskShouldFlattenDailyLoss()
  {
   return (InpCloseOnDailyLoss && g_state.dailyLossHalt && BasketCount() > 0);
  }

//+------------------------------------------------------------------+
double RiskNormalizeLot(double lot)
  {
   const double minLotSym = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   const double maxLotSym = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   const double step      = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);

   double minLot = minLotSym;
   if(InpMinLotOverride > 0.0)
      minLot = MathMax(minLotSym, InpMinLotOverride);

   double maxLot = MathMin(maxLotSym, InpMaxLot);

   if(step > 0.0)
      lot = MathFloor(lot / step + 1e-12) * step;

   if(lot < minLot)
      lot = minLot;
   if(lot > maxLot)
      lot = maxLot;

   int digits = 2;
   if(step > 0.0 && step < 1.0)
      digits = (int)MathMax(0, MathRound(-MathLog10(step)));
   return NormalizeDouble(lot, digits > 8 ? 8 : digits);
  }

//+------------------------------------------------------------------+
double RiskLotFromPercent()
  {
   if(InpSL_Points <= 0 || InpRiskPercent <= 0.0)
      return InpLot;

   const double base = RiskAccountBase();
   const double riskMoney = base * InpRiskPercent / 100.0;

   const double tickSize  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   const double tickValue = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   const double point     = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   if(tickSize <= 0.0 || tickValue <= 0.0 || point <= 0.0)
      return InpLot;

   const double lossPerLot = ((double)InpSL_Points * point / tickSize) * tickValue;
   if(lossPerLot <= 0.0)
      return InpLot;

   return riskMoney / lossPerLot;
  }

//+------------------------------------------------------------------+
double RiskLot()
  {
   double lot = InpLot;
   if(InpLotMode == BMRG_LOT_RISK_PCT)
      lot = RiskLotFromPercent();
   const double aosMult = AOSLotMultiplier();
   if(aosMult <= 0.0)
      return 0.0;
   if(aosMult < 1.0)
      lot *= aosMult;
   return RiskNormalizeLot(lot);
  }

//+------------------------------------------------------------------+
double RiskStopLossPrice(const ENUM_BMRG_SIDE side, const double entryPrice)
  {
   if(InpSL_Points <= 0)
      return 0.0;

   const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   const double dist  = (double)InpSL_Points * point;
   const int digits   = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);

   if(side == BMRG_SIDE_BUY)
      return NormalizeDouble(entryPrice - dist, digits);
   if(side == BMRG_SIDE_SELL)
      return NormalizeDouble(entryPrice + dist, digits);
   return 0.0;
  }

//+------------------------------------------------------------------+
double RiskTakeProfitPrice(const ENUM_BMRG_SIDE side, const double entryPrice)
  {
   if(InpTP_Points <= 0)
      return 0.0;

   const double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   const double dist  = (double)InpTP_Points * point;
   const int digits   = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);

   if(side == BMRG_SIDE_BUY)
      return NormalizeDouble(entryPrice + dist, digits);
   if(side == BMRG_SIDE_SELL)
      return NormalizeDouble(entryPrice - dist, digits);
   return 0.0;
  }

#endif // BMRG_RISK_MQH
