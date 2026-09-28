//+------------------------------------------------------------------+
//| Basket.mqh — positions by magic + symbol                           |
//+------------------------------------------------------------------+
#ifndef BMRG_BASKET_MQH
#define BMRG_BASKET_MQH

#include "Config.mqh"
#include "State.mqh"
#include "Logger.mqh"

//+------------------------------------------------------------------+
bool BasketIsOurs(const ulong ticket)
  {
   if(!PositionSelectByTicket(ticket))
      return false;
   if(PositionGetString(POSITION_SYMBOL) != _Symbol)
      return false;
   if((long)PositionGetInteger(POSITION_MAGIC) != InpMagic)
      return false;
   return true;
  }

//+------------------------------------------------------------------+
int BasketCount()
  {
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;
      if(BasketIsOurs(ticket))
         count++;
     }
   return count;
  }

//+------------------------------------------------------------------+
ENUM_BMRG_SIDE BasketSideFromMarket()
  {
   bool hasBuy = false;
   bool hasSell = false;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !BasketIsOurs(ticket))
         continue;

      const long type = PositionGetInteger(POSITION_TYPE);
      if(type == POSITION_TYPE_BUY)
         hasBuy = true;
      else if(type == POSITION_TYPE_SELL)
         hasSell = true;
     }

   if(hasBuy && hasSell)
     {
      LogWarn("Basket has both sides — Phase 1 expects one direction; using BUY");
      return BMRG_SIDE_BUY;
     }
   if(hasBuy)
      return BMRG_SIDE_BUY;
   if(hasSell)
      return BMRG_SIDE_SELL;
   return BMRG_SIDE_NONE;
  }

//+------------------------------------------------------------------+
// Rebuild g_state from open positions (restart recovery).
void BasketRebuildState()
  {
   g_state.entryCount = BasketCount();
   g_state.basketSide = BasketSideFromMarket();
   g_state.levelsFilled = g_state.entryCount; // Phase 1: 1 entry ≈ 1 level
   if(g_state.levelsFilled > InpMaxLevels)
      g_state.levelsFilled = InpMaxLevels;

   LogInfo(StringFormat(
              "Basket rebuild: side=%s entries=%d levelsFilled=%d",
              SideToString(g_state.basketSide),
              g_state.entryCount,
              g_state.levelsFilled));
  }

//+------------------------------------------------------------------+
// Collect our tickets into array (as series-friendly dynamic).
int BasketCollectTickets(ulong &tickets[])
  {
   ArrayResize(tickets, 0);
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      const ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !BasketIsOurs(ticket))
         continue;
      const int n = ArraySize(tickets);
      ArrayResize(tickets, n + 1);
      tickets[n] = ticket;
     }
   return ArraySize(tickets);
  }

#endif // BMRG_BASKET_MQH
