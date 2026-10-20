//+------------------------------------------------------------------+
//| Signal.mqh — closed-bar entry / exit (+ optional fade confirm)     |
//+------------------------------------------------------------------+
#ifndef BMRG_SIGNAL_MQH
#define BMRG_SIGNAL_MQH

#include "Config.mqh"
#include "State.mqh"
#include "Indicators.mqh"
#include "Grid.mqh"
#include "Logger.mqh"

enum ENUM_BMRG_SIGNAL
  {
   BMRG_SIG_NONE = 0,
   BMRG_SIG_ENTER_BUY,
   BMRG_SIG_ENTER_SELL,
   BMRG_SIG_EXIT
  };

struct SignalResult
  {
   ENUM_BMRG_SIGNAL type;
   ENUM_BMRG_SIDE   side;
   int              levelIndex;
   string           reason;
  };

//+------------------------------------------------------------------+
void SignalClear(SignalResult &sig)
  {
   sig.type = BMRG_SIG_NONE;
   sig.side = BMRG_SIDE_NONE;
   sig.levelIndex = -1;
   sig.reason = "";
  }

//+------------------------------------------------------------------+
void SignalArmFadeSetup(const ENUM_BMRG_SIDE side, const int levelIndex, const datetime barTime)
  {
   g_state.fadeSetupSide = side;
   g_state.fadeSetupLevel = levelIndex;
   g_state.fadeSetupAgeBars = 0;
   g_state.fadeSetupBarTime = barTime;
  }

//+------------------------------------------------------------------+
// Reclaim: close back inside the extreme level, optionally still on
// the setup side of mid (toward-mean confirmation, not already through mid).
bool SignalFadeConfirmed(const BandValues &bands, const ENUM_BMRG_SIDE side, const int levelIndex)
  {
   double levelPrice = 0.0;
   if(!GridLevelPrice(bands, side, levelIndex, levelPrice))
      return false;

   if(side == BMRG_SIDE_BUY)
     {
      // Was at/below lower → confirm when close back above that level
      if(bands.close <= levelPrice)
         return false;
      if(InpFadeRequireInsideMid && bands.close >= bands.mid)
         return false;
      return true;
     }
   if(side == BMRG_SIDE_SELL)
     {
      if(bands.close >= levelPrice)
         return false;
      if(InpFadeRequireInsideMid && bands.close <= bands.mid)
         return false;
      return true;
     }
   return false;
  }

//+------------------------------------------------------------------+
// Flat-book path with setup → reclaim gate (raises WR vs touch-entry).
SignalResult SignalEvaluateFadeConfirm(const BandValues &bands, const int nextLevel)
  {
   SignalResult sig;
   SignalClear(sig);

   const datetime bar1 = iTime(_Symbol, _Period, 1);
   const bool buyHit  = InpAllowBuy  && GridPriceReached(bands, BMRG_SIDE_BUY,  nextLevel);
   const bool sellHit = InpAllowSell && GridPriceReached(bands, BMRG_SIDE_SELL, nextLevel);

   // Age / expire pending setup on each new closed bar (barTime advances so re-entry same bar won't double-count)
   if(g_state.fadeSetupSide != BMRG_SIDE_NONE)
     {
      if(bar1 != 0 && g_state.fadeSetupBarTime != 0 && bar1 != g_state.fadeSetupBarTime)
        {
         g_state.fadeSetupAgeBars++;
         g_state.fadeSetupBarTime = bar1;
        }

      if(g_state.fadeSetupAgeBars > InpFadeConfirmMaxBars)
        {
         if(InpLogGateBlocks)
            LogInfo(StringFormat(
                       "Fade setup expired side=%s age=%d max=%d",
                       SideToString(g_state.fadeSetupSide),
                       g_state.fadeSetupAgeBars,
                       InpFadeConfirmMaxBars));
         StateClearFadeSetup();
        }
     }

   if(buyHit && sellHit)
     {
      StateClearFadeSetup();
      sig.reason = "ambiguous both sides; skip";
      return sig;
     }

   // Pending BUY setup
   if(g_state.fadeSetupSide == BMRG_SIDE_BUY)
     {
      if(sellHit)
        {
         // Opposite extreme: flip setup
         SignalArmFadeSetup(BMRG_SIDE_SELL, nextLevel, bar1);
         sig.reason = "fade setup flip → SELL L" + IntegerToString(nextLevel);
         return sig;
        }
      // Same-bar as arm: never confirm (still the extreme print)
      if(g_state.fadeSetupAgeBars >= 1 &&
         SignalFadeConfirmed(bands, BMRG_SIDE_BUY, g_state.fadeSetupLevel))
        {
         sig.type = BMRG_SIG_ENTER_BUY;
         sig.side = BMRG_SIDE_BUY;
         sig.levelIndex = g_state.fadeSetupLevel;
         sig.reason = "enter buy L" + IntegerToString(sig.levelIndex) + " fade-confirm";
         StateClearFadeSetup();
         return sig;
        }
      if(buyHit)
        {
         // Still outside: keep waiting (age already ticking)
         sig.reason = "fade setup BUY waiting reclaim";
         return sig;
        }
      sig.reason = "fade setup BUY waiting reclaim";
      return sig;
     }

   // Pending SELL setup
   if(g_state.fadeSetupSide == BMRG_SIDE_SELL)
     {
      if(buyHit)
        {
         SignalArmFadeSetup(BMRG_SIDE_BUY, nextLevel, bar1);
         sig.reason = "fade setup flip → BUY L" + IntegerToString(nextLevel);
         return sig;
        }
      if(g_state.fadeSetupAgeBars >= 1 &&
         SignalFadeConfirmed(bands, BMRG_SIDE_SELL, g_state.fadeSetupLevel))
        {
         sig.type = BMRG_SIG_ENTER_SELL;
         sig.side = BMRG_SIDE_SELL;
         sig.levelIndex = g_state.fadeSetupLevel;
         sig.reason = "enter sell L" + IntegerToString(sig.levelIndex) + " fade-confirm";
         StateClearFadeSetup();
         return sig;
        }
      sig.reason = "fade setup SELL waiting reclaim";
      return sig;
     }

   // No setup: arm on extreme touch (do not enter yet)
   if(buyHit)
     {
      SignalArmFadeSetup(BMRG_SIDE_BUY, nextLevel, bar1);
      sig.reason = "fade setup armed BUY L" + IntegerToString(nextLevel);
      return sig;
     }
   if(sellHit)
     {
      SignalArmFadeSetup(BMRG_SIDE_SELL, nextLevel, bar1);
      sig.reason = "fade setup armed SELL L" + IntegerToString(nextLevel);
      return sig;
     }

   sig.reason = "no signal";
   return sig;
  }

//+------------------------------------------------------------------+
SignalResult SignalEvaluate(const BandValues &bands,
                            const ENUM_BMRG_SIDE basketSide,
                            const int levelsFilled)
  {
   SignalResult sig;
   SignalClear(sig);

   if(!bands.valid)
     {
      sig.reason = "bands invalid";
      return sig;
     }

   // Meanrev mode (TP off): exit when price returns to mid.
   // Geometry mode (InpTP_Points > 0): skip mid-exit — broker SL/TP define RR.
   if(InpTP_Points <= 0)
     {
      if(basketSide == BMRG_SIDE_BUY && bands.close >= bands.mid)
        {
         sig.type = BMRG_SIG_EXIT;
         sig.side = BMRG_SIDE_BUY;
         sig.reason = "close>=mid exit long";
         return sig;
        }
      if(basketSide == BMRG_SIDE_SELL && bands.close <= bands.mid)
        {
         sig.type = BMRG_SIG_EXIT;
         sig.side = BMRG_SIDE_SELL;
         sig.reason = "close<=mid exit short";
         return sig;
        }
     }

   const int nextLevel = GridNextLevelIndex(levelsFilled);
   if(nextLevel < 0)
     {
      sig.reason = "max levels filled";
      return sig;
     }

   // Fade confirm only for flat first entry (G0). Grid adds stay immediate.
   if(InpUseFadeConfirm && basketSide == BMRG_SIDE_NONE)
      return SignalEvaluateFadeConfirm(bands, nextLevel);

   // Basket open or fade-confirm OFF: clear any stale setup
   if(basketSide != BMRG_SIDE_NONE)
      StateClearFadeSetup();

   const bool buyHit  = InpAllowBuy  && GridPriceReached(bands, BMRG_SIDE_BUY,  nextLevel);
   const bool sellHit = InpAllowSell && GridPriceReached(bands, BMRG_SIDE_SELL, nextLevel);

   // Flat: open at most one side; skip if both hit same bar
   if(basketSide == BMRG_SIDE_NONE)
     {
      if(buyHit && sellHit)
        {
         sig.reason = "ambiguous both sides; skip";
         return sig;
        }
      if(buyHit)
        {
         sig.type = BMRG_SIG_ENTER_BUY;
         sig.side = BMRG_SIDE_BUY;
         sig.levelIndex = nextLevel;
         sig.reason = "enter buy L" + IntegerToString(nextLevel);
         return sig;
        }
      if(sellHit)
        {
         sig.type = BMRG_SIG_ENTER_SELL;
         sig.side = BMRG_SIDE_SELL;
         sig.levelIndex = nextLevel;
         sig.reason = "enter sell L" + IntegerToString(nextLevel);
         return sig;
        }
      sig.reason = "no signal";
      return sig;
     }

   // Basket open: same-side add only; ignore opposite
   if(basketSide == BMRG_SIDE_BUY)
     {
      if(buyHit)
        {
         sig.type = BMRG_SIG_ENTER_BUY;
         sig.side = BMRG_SIDE_BUY;
         sig.levelIndex = nextLevel;
         sig.reason = "add buy L" + IntegerToString(nextLevel);
         return sig;
        }
      sig.reason = sellHit ? "opposite sell ignored" : "no signal";
      return sig;
     }

   if(basketSide == BMRG_SIDE_SELL)
     {
      if(sellHit)
        {
         sig.type = BMRG_SIG_ENTER_SELL;
         sig.side = BMRG_SIDE_SELL;
         sig.levelIndex = nextLevel;
         sig.reason = "add sell L" + IntegerToString(nextLevel);
         return sig;
        }
      sig.reason = buyHit ? "opposite buy ignored" : "no signal";
      return sig;
     }

   sig.reason = "no signal";
   return sig;
  }

#endif // BMRG_SIGNAL_MQH
