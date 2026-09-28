//+------------------------------------------------------------------+
//| Grid.mqh — σ-based level map                                       |
//+------------------------------------------------------------------+
#ifndef BMRG_GRID_MQH
#define BMRG_GRID_MQH

#include "Config.mqh"
#include "Indicators.mqh"
#include "State.mqh"

//+------------------------------------------------------------------+
// Deviation multiplier for 0-based level index.
double GridLevelSigma(const int levelIndex)
  {
   return InpBBDev + (double)levelIndex * InpLevelStepSigma;
  }

//+------------------------------------------------------------------+
// Next free level index given how many levels already filled.
int GridNextLevelIndex(const int levelsFilled)
  {
   if(levelsFilled < 0)
      return 0;
   if(levelsFilled >= InpMaxLevels)
      return -1;
   return levelsFilled;
  }

//+------------------------------------------------------------------+
// Price target for a long (below mid) or short (above mid) level.
bool GridLevelPrice(const BandValues &bands,
                    const ENUM_BMRG_SIDE side,
                    const int levelIndex,
                    double &priceOut)
  {
   priceOut = 0.0;
   double sigma = 0.0;
   if(!IndicatorsSigma(bands, sigma))
      return false;
   if(levelIndex < 0 || levelIndex >= InpMaxLevels)
      return false;

   const double k = GridLevelSigma(levelIndex);
   if(side == BMRG_SIDE_BUY)
     {
      priceOut = bands.mid - k * sigma;
      return true;
     }
   if(side == BMRG_SIDE_SELL)
     {
      priceOut = bands.mid + k * sigma;
      return true;
     }
   return false;
  }

//+------------------------------------------------------------------+
// True when closed price has reached the level (deep enough).
bool GridPriceReached(const BandValues &bands,
                      const ENUM_BMRG_SIDE side,
                      const int levelIndex)
  {
   double levelPrice = 0.0;
   if(!GridLevelPrice(bands, side, levelIndex, levelPrice))
      return false;

   if(side == BMRG_SIDE_BUY)
      return (bands.close <= levelPrice);
   if(side == BMRG_SIDE_SELL)
      return (bands.close >= levelPrice);
   return false;
  }

#endif // BMRG_GRID_MQH
