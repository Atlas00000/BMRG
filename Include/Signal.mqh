//+------------------------------------------------------------------+
//| Signal.mqh — closed-bar entry / exit                               |
//+------------------------------------------------------------------+
#ifndef BMRG_SIGNAL_MQH
#define BMRG_SIGNAL_MQH

#include "Config.mqh"
#include "State.mqh"
#include "Indicators.mqh"
#include "Grid.mqh"

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
