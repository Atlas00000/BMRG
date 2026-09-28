//+------------------------------------------------------------------+
//| BMRG.mq5 — Bollinger Mean-Reversion Grid                           |
//| Execution engine + filters, regimes, risk%, exposure, containment  |
//+------------------------------------------------------------------+
#property copyright "BMRG Phase 1 + AOS INF"
#property version   "1.21"

#include "Include/Config.mqh"
#include "Include/Logger.mqh"
#include "Include/State.mqh"
#include "Include/Indicators.mqh"
#include "Include/Filters.mqh"
#include "Include/Grid.mqh"
#include "Include/Signal.mqh"
#include "Include/Basket.mqh"
#include "Include/Risk.mqh"
#include "Include/AOS.mqh"
#include "Include/Execution.mqh"

//+------------------------------------------------------------------+
int OnInit()
  {
   string reason = "";
   if(!ConfigValidate(reason))
     {
      LogError("Init refused: " + reason);
      return INIT_FAILED;
     }

   StateInit();

   if(!IndicatorsInit())
      return INIT_FAILED;

   ExecutionInit();
   BasketRebuildState();
   AOSInit();

   LogInfo(StringFormat(
              "BMRG init OK | %s %s | BB(%d,%.1f) ATR(%d) lotMode=%d lot=%.2f risk%%=%.2f maxExp%%=%.1f magic=%d aos=%d",
              _Symbol, EnumToString(_Period),
              InpBBPeriod, InpBBDev, InpATRPeriod,
              (int)InpLotMode, InpLot, InpRiskPercent, InpMaxExposurePct, (int)InpMagic,
              (int)InpAOS_Enable));

   LogCommentUpdate(InpAOS_Enable ? "BMRG+AOS ready" : "BMRG ready");
   return INIT_SUCCEEDED;
  }

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   AOSDeinit();
   IndicatorsRelease();
   Comment("");
   LogInfo("BMRG deinit reason=" + IntegerToString(reason));
  }

//+------------------------------------------------------------------+
bool IsNewBar()
  {
   const datetime t = iTime(_Symbol, _Period, 0);
   if(t == 0)
      return false;
   if(t == g_state.lastBarTime)
      return false;
   g_state.lastBarTime = t;
   return true;
  }

//+------------------------------------------------------------------+
void LogBarSnapshot(const BandValues &bands, const SignalResult &sig)
  {
   const datetime bar1 = iTime(_Symbol, _Period, 1);
   LogInfo(StringFormat(
              "bar=%s U=%.5f M=%.5f L=%.5f C=%.5f ATR=%.1fpt BBw=%.2f%% side=%s n=%d sig=%d %s spr=%d halt=%d pause=%d",
              TimeToString(bar1, TIME_DATE|TIME_MINUTES),
              bands.upper, bands.mid, bands.lower, bands.close,
              IndicatorsATRPoints(bands), bands.bbWidthPct,
              SideToString(g_state.basketSide),
              g_state.entryCount,
              (int)sig.type,
              sig.reason,
              RiskCurrentSpreadPoints(),
              (int)g_state.equityHalt,
              (int)g_state.failPause));

   LogCommentUpdate(StringFormat(
                       "BMRG %s n=%d | ddDay halt=%d pause=%d | %s | %s",
                       SideToString(g_state.basketSide),
                       g_state.entryCount,
                       (int)g_state.dailyLossHalt,
                       (int)g_state.failPause,
                       sig.reason,
                       AOSStatusLine()));
  }

//+------------------------------------------------------------------+
void ProcessClosedBar()
  {
   StateRollDayIfNeeded();
   RiskTickFailPause();

   BandValues bands;
   if(!IndicatorsRead(1, bands))
     {
      LogWarn("IndicatorsRead shift1 failed");
      return;
     }

   BasketRebuildState();
   RiskUpdateEquityHalt();
   RiskUpdateDailyLossHalt();
   AOSUpdateObserver();

   // Failure containment: optional flatten on daily loss
   if(RiskShouldFlattenDailyLoss())
     {
      string flatReason = "";
      LogWarn("Flatten on daily loss halt");
      ExecutionCloseAll(flatReason);
      return;
     }

   SignalResult sig = SignalEvaluate(bands, g_state.basketSide, g_state.levelsFilled);
   LogBarSnapshot(bands, sig);

   string reason = "";

   if(sig.type == BMRG_SIG_EXIT)
     {
      if(!ExecutionCloseAll(reason))
         LogWarn("Exit incomplete: " + reason);
      return;
     }

   if(sig.type == BMRG_SIG_ENTER_BUY || sig.type == BMRG_SIG_ENTER_SELL)
     {
      if(!RiskCanOpenNewEntry(bands, reason))
        {
         if(InpLogGateBlocks)
            LogInfo("Entry blocked: " + reason);
         return;
        }

      const ENUM_BMRG_SIDE side =
         (sig.type == BMRG_SIG_ENTER_BUY) ? BMRG_SIDE_BUY : BMRG_SIDE_SELL;

      if(!AOSAllowEntry(side, reason))
        {
         if(InpLogGateBlocks)
            LogInfo("Entry blocked: " + reason);
         return;
        }

      if(!ExecutionOpen(side, sig.levelIndex, reason))
         LogWarn("Entry failed: " + reason);
     }
  }

//+------------------------------------------------------------------+
void OnTick()
  {
   if(!IsNewBar())
      return;
   ProcessClosedBar();
  }

//+------------------------------------------------------------------+
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result)
  {
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD)
      return;
   if(trans.symbol != _Symbol)
      return;
   if(trans.deal == 0 || !HistoryDealSelect(trans.deal))
      return;
   if((long)HistoryDealGetInteger(trans.deal, DEAL_MAGIC) != InpMagic)
      return;

   g_state.lastDealTicket = trans.deal;

   const long entry = HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
   if(entry == DEAL_ENTRY_OUT || entry == DEAL_ENTRY_OUT_BY || entry == DEAL_ENTRY_INOUT)
     {
      const double profit = HistoryDealGetDouble(trans.deal, DEAL_PROFIT)
                            + HistoryDealGetDouble(trans.deal, DEAL_SWAP)
                            + HistoryDealGetDouble(trans.deal, DEAL_COMMISSION);
      RiskOnClosedDealProfit(profit);
      AOSOnClosedDeal(profit);
     }

   BasketRebuildState();
  }

//+------------------------------------------------------------------+
