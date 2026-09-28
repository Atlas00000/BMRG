//+------------------------------------------------------------------+
//| Logger.mqh — structured Print / optional Comment                   |
//+------------------------------------------------------------------+
#ifndef BMRG_LOGGER_MQH
#define BMRG_LOGGER_MQH

#include "Config.mqh"

string g_logLastComment = "";

//+------------------------------------------------------------------+
void LogInfo(const string msg)
  {
   Print("[BMRG][INFO] ", msg);
  }

//+------------------------------------------------------------------+
void LogWarn(const string msg)
  {
   Print("[BMRG][WARN] ", msg);
  }

//+------------------------------------------------------------------+
void LogError(const string msg)
  {
   Print("[BMRG][ERROR] ", msg);
  }

//+------------------------------------------------------------------+
void LogTrade(const string msg)
  {
   Print("[BMRG][TRADE] ", msg);
  }

//+------------------------------------------------------------------+
void LogCommentUpdate(const string line)
  {
   g_logLastComment = line;
   if(InpLogToComment)
      Comment(line);
  }

#endif // BMRG_LOGGER_MQH
