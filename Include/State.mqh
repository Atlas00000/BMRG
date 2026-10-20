//+------------------------------------------------------------------+
//| State.mqh — runtime + daily / failure containment                  |
//+------------------------------------------------------------------+
#ifndef BMRG_STATE_MQH
#define BMRG_STATE_MQH

enum ENUM_BMRG_SIDE
  {
   BMRG_SIDE_NONE = 0,
   BMRG_SIDE_BUY  = 1,
   BMRG_SIDE_SELL = 2
  };

struct BMRGState
  {
   datetime        lastBarTime;
   bool            equityHalt;
   bool            dailyLossHalt;
   bool            failPause;
   double          startEquity;
   double          dayStartEquity;
   int             dayStamp;          // yyyymmdd
   int             dailyEntries;
   ENUM_BMRG_SIDE  basketSide;
   int             entryCount;
   int             levelsFilled;
   datetime        lastEntryBarTime;
   ulong           lastDealTicket;
   string          lastAction;
   // fade confirm (setup → reclaim)
   ENUM_BMRG_SIDE  fadeSetupSide;
   int             fadeSetupLevel;
   int             fadeSetupAgeBars;   // closed bars since arm (0 = armed this bar)
   datetime        fadeSetupBarTime;
   // failure containment
   int             consecOrderFails;
   int             consecLosses;
   int             pauseBarsLeft;
   string          pauseReason;
  };

BMRGState g_state;

//+------------------------------------------------------------------+
int StateDayStamp(const datetime t)
  {
   MqlDateTime dt;
   TimeToStruct(t, dt);
   return dt.year * 10000 + dt.mon * 100 + dt.day;
  }

//+------------------------------------------------------------------+
void StateInit()
  {
   ZeroMemory(g_state);
   g_state.basketSide = BMRG_SIDE_NONE;
   g_state.startEquity = AccountInfoDouble(ACCOUNT_EQUITY);
   g_state.dayStartEquity = g_state.startEquity;
   g_state.dayStamp = StateDayStamp(TimeCurrent());
   g_state.lastAction = "init";
   g_state.pauseReason = "";
   g_state.fadeSetupSide = BMRG_SIDE_NONE;
   g_state.fadeSetupLevel = -1;
   g_state.fadeSetupAgeBars = 0;
   g_state.fadeSetupBarTime = 0;
  }

//+------------------------------------------------------------------+
void StateClearFadeSetup()
  {
   g_state.fadeSetupSide = BMRG_SIDE_NONE;
   g_state.fadeSetupLevel = -1;
   g_state.fadeSetupAgeBars = 0;
   g_state.fadeSetupBarTime = 0;
  }

//+------------------------------------------------------------------+
void StateRollDayIfNeeded()
  {
   const int today = StateDayStamp(TimeCurrent());
   if(today == g_state.dayStamp)
      return;

   g_state.dayStamp = today;
   g_state.dayStartEquity = AccountInfoDouble(ACCOUNT_EQUITY);
   g_state.dailyEntries = 0;
   g_state.dailyLossHalt = false;
  }

//+------------------------------------------------------------------+
string SideToString(const ENUM_BMRG_SIDE side)
  {
   if(side == BMRG_SIDE_BUY)
      return "BUY";
   if(side == BMRG_SIDE_SELL)
      return "SELL";
   return "NONE";
  }

#endif // BMRG_STATE_MQH
