//+------------------------------------------------------------------+
//| Execution.mqh — market orders, fail closed, containment hooks      |
//+------------------------------------------------------------------+
#ifndef BMRG_EXECUTION_MQH
#define BMRG_EXECUTION_MQH

#include <Trade/Trade.mqh>
#include "Config.mqh"
#include "State.mqh"
#include "Logger.mqh"
#include "Basket.mqh"
#include "Risk.mqh"

CTrade g_trade;

//+------------------------------------------------------------------+
void ExecutionInit()
  {
   g_trade.SetExpertMagicNumber((ulong)InpMagic);
   g_trade.SetDeviationInPoints((ulong)InpSlippage);
   g_trade.SetAsyncMode(false);

   const long fill = SymbolInfoInteger(_Symbol, SYMBOL_FILLING_MODE);
   if((fill & SYMBOL_FILLING_IOC) == SYMBOL_FILLING_IOC)
      g_trade.SetTypeFilling(ORDER_FILLING_IOC);
   else if((fill & SYMBOL_FILLING_FOK) == SYMBOL_FILLING_FOK)
      g_trade.SetTypeFilling(ORDER_FILLING_FOK);
   else
      g_trade.SetTypeFilling(ORDER_FILLING_RETURN);
  }

//+------------------------------------------------------------------+
bool ExecutionStopsDistanceOk(const ENUM_BMRG_SIDE side,
                              const double price,
                              const double sl,
                              const double tp,
                              string &reason)
  {
   reason = "";
   const int stopsLevel = (int)SymbolInfoInteger(_Symbol, SYMBOL_TRADE_STOPS_LEVEL);
   const double point   = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   const double minDist = (double)stopsLevel * point;

   if(sl != 0.0)
     {
      if(side == BMRG_SIDE_BUY && (price - sl) < minDist)
        {
         reason = "SL too close (buy)";
         return false;
        }
      if(side == BMRG_SIDE_SELL && (sl - price) < minDist)
        {
         reason = "SL too close (sell)";
         return false;
        }
     }
   if(tp != 0.0)
     {
      if(side == BMRG_SIDE_BUY && (tp - price) < minDist)
        {
         reason = "TP too close (buy)";
         return false;
        }
      if(side == BMRG_SIDE_SELL && (price - tp) < minDist)
        {
         reason = "TP too close (sell)";
         return false;
        }
     }
   return true;
  }

//+------------------------------------------------------------------+
bool ExecutionOpen(const ENUM_BMRG_SIDE side, const int levelIndex, string &reason)
  {
   reason = "";
   const double lot = RiskLot();
   if(lot <= 0.0)
     {
      reason = "invalid lot";
      RiskOnOrderFail();
      return false;
     }

   double price = 0.0;
   if(side == BMRG_SIDE_BUY)
      price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   else if(side == BMRG_SIDE_SELL)
      price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   else
     {
      reason = "invalid side";
      return false;
     }

   const double sl = RiskStopLossPrice(side, price);
   const double tp = RiskTakeProfitPrice(side, price);
   if(!ExecutionStopsDistanceOk(side, price, sl, tp, reason))
     {
      LogWarn(reason);
      RiskOnOrderFail();
      return false;
     }

   // Pre-check margin for this lot
   double needMargin = 0.0;
   const ENUM_ORDER_TYPE otype = (side == BMRG_SIDE_BUY) ? ORDER_TYPE_BUY : ORDER_TYPE_SELL;
   if(!OrderCalcMargin(otype, _Symbol, lot, price, needMargin))
     {
      reason = "OrderCalcMargin failed";
      RiskOnOrderFail();
      return false;
     }
   if(needMargin > AccountInfoDouble(ACCOUNT_MARGIN_FREE))
     {
      reason = StringFormat("insufficient margin need=%.2f free=%.2f",
                            needMargin, AccountInfoDouble(ACCOUNT_MARGIN_FREE));
      RiskOnOrderFail();
      return false;
     }

   const string comment = StringFormat("BMRG L%d", levelIndex);
   bool ok = false;
   if(side == BMRG_SIDE_BUY)
      ok = g_trade.Buy(lot, _Symbol, price, sl, tp, comment);
   else
      ok = g_trade.Sell(lot, _Symbol, price, sl, tp, comment);

   if(!ok)
     {
      reason = StringFormat("OrderSend fail retcode=%u err=%d",
                            g_trade.ResultRetcode(), GetLastError());
      LogError(reason);
      RiskOnOrderFail();
      return false;
     }

   RiskOnOrderSuccess();
   StateRollDayIfNeeded();
   g_state.dailyEntries++;
   g_state.lastEntryBarTime = iTime(_Symbol, _Period, 0);
   g_state.basketSide = side;
   g_state.entryCount = BasketCount();
   g_state.levelsFilled++;
   if(g_state.levelsFilled > InpMaxLevels)
      g_state.levelsFilled = InpMaxLevels;
   g_state.lastAction = comment;

   LogTrade(StringFormat(
               "OPEN %s lot=%.2f price=%.5f sl=%.5f tp=%.5f level=%d riskMode=%d spread=%d deal=%s",
               SideToString(side), lot, g_trade.ResultPrice(), sl, tp, levelIndex,
               (int)InpLotMode, RiskCurrentSpreadPoints(),
               IntegerToString((long)g_trade.ResultDeal())));
   return true;
  }

//+------------------------------------------------------------------+
bool ExecutionCloseAll(string &reason)
  {
   reason = "";
   ulong tickets[];
   const int n = BasketCollectTickets(tickets);
   if(n == 0)
     {
      reason = "no positions";
      g_state.basketSide = BMRG_SIDE_NONE;
      g_state.entryCount = 0;
      g_state.levelsFilled = 0;
      return true;
     }

   int closed = 0;
   for(int i = 0; i < n; i++)
     {
      if(!g_trade.PositionClose(tickets[i]))
        {
         LogError(StringFormat("Close fail ticket=%s retcode=%u",
                               IntegerToString((long)tickets[i]), g_trade.ResultRetcode()));
         RiskOnOrderFail();
         continue;
        }
      RiskOnOrderSuccess();
      closed++;
     }

   BasketRebuildState();

   if(closed == 0)
     {
      reason = "close all failed";
      return false;
     }

   LogTrade(StringFormat("CLOSE basket closed=%d/%d remaining=%d", closed, n, BasketCount()));
   g_state.lastAction = "exit";
   return (BasketCount() == 0);
  }

#endif // BMRG_EXECUTION_MQH
