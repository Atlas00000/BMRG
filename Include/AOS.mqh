//+------------------------------------------------------------------+
//| AOS.mqh — AI OS layers L2–L6 wired for Strategy Tester / live      |
//| L1 features at signal · L2det via Filters · L2 AI L2skip_v1        |
//| L3 halt Below-frontier / MaxDD · L4 lifecycle size · L6 ledger     |
//+------------------------------------------------------------------+
#ifndef BMRG_AOS_MQH
#define BMRG_AOS_MQH

#include "Config.mqh"
#include "State.mqh"
#include "Logger.mqh"
#include "AOS_L2skip_inf.mqh"
#include "AOS_L2skip_aud.mqh"
#include "AOS_L2det_aapl.mqh"
#include "AOS_L2det_aapl_m5.mqh"
#include "AOS_L2det_uk.mqh"
#include "AOS_L2det_eur.mqh"
#include "AOS_L2det_aud.mqh"
#include "AOS_L2det_de.mqh"
#include "AOS_L2det_de_m5.mqh"
#include "AOS_L2det_jp.mqh"
#include "AOS_L2det_jp_m5.mqh"
#include "AOS_L2det_usdjpy.mqh"

//+------------------------------------------------------------------+
bool AOSIsAudUsd()
  {
   return (StringFind(_Symbol, "AUDUSD") == 0);
  }

//+------------------------------------------------------------------+
string AOSActiveL2Semver()
  {
   if(AOSIsUk100Symbol())
      return AOS_L2DET_UK_SEMVER;
   if(AOSIsAppleSymbol() && Period() == PERIOD_M5 && InpAOS_AAPL_M5_L2detEnable)
      return AOS_L2DET_AAPL_M5_SEMVER;
   if(AOSIsAppleSymbol())
      return AOS_L2DET_AAPL_SEMVER;
   if(AOSIsEurUsdSymbol() && InpAOS_EUR_L2detEnable)
      return AOS_L2DET_EUR_SEMVER;
   if(AOSIsAudUsd() && InpAOS_AUD_L2detEnable)
      return AOS_L2DET_AUD_SEMVER;
   if(AOSIsDe40Symbol() && Period() == PERIOD_M5 && InpAOS_DE_M5_L2detEnable)
      return AOS_L2DET_DE_M5_SEMVER;
   if(AOSIsDe40Symbol() && Period() != PERIOD_M5 && InpAOS_DE_L2detEnable)
      return AOS_L2DET_DE_SEMVER;
   if(AOSIsJp225Symbol() && Period() == PERIOD_M5 && InpAOS_JP_M5_L2detEnable)
      return AOS_L2DET_JP_M5_SEMVER;
   if(AOSIsJp225Symbol() && Period() != PERIOD_M5 && InpAOS_JP_L2detEnable)
      return AOS_L2DET_JP_SEMVER;
   if(AOSIsUsdJpySymbol() && InpAOS_USDJPY_L2detEnable)
      return AOS_L2DET_USDJPY_SEMVER;
   return AOSIsAudUsd() ? AOS_L2AUD_SEMVER : AOS_L2INF_SEMVER;
  }

#define AOS_RING_MAX 600

enum ENUM_AOS_LIFE
  {
   AOS_LIFE_EXPANDING = 0,
   AOS_LIFE_STABLE,
   AOS_LIFE_COMPRESSING,
   AOS_LIFE_NEAR,
   AOS_LIFE_BELOW
  };

struct AOSRuntime
  {
   bool              inited;
   bool              haltL3;
   bool              deriskL3;
   string            haltReason;
   string            lastL2Reason;
   double            peakEquity;
   double            fRec;           // L4 size multiplier 0..1
   double            w250EF;
   double            w250EN;
   double            w250WR;
   double            lastAIProba;
   bool              lastAISkip;
   ENUM_AOS_LIFE     life;
   // ring of closed outcomes: 1=TP/win, 0=SL/loss
   int               ring[AOS_RING_MAX];
   int               ringN;
   int               ringHead;       // next write index
   int               ledgerHandle;
  };

AOSRuntime g_aos;

//+------------------------------------------------------------------+
string AOSLifeToString(const ENUM_AOS_LIFE life)
  {
   switch(life)
     {
      case AOS_LIFE_EXPANDING:   return "Expanding";
      case AOS_LIFE_STABLE:      return "Stable";
      case AOS_LIFE_COMPRESSING: return "Compressing";
      case AOS_LIFE_NEAR:        return "Near";
      case AOS_LIFE_BELOW:       return "Below";
     }
   return "Stable";
  }

//+------------------------------------------------------------------+
// Effective L2 mode: kill-switch forces OFF; else InpAiOsMode;
// legacy InpAOS_L2AI_* used only when InpAiOsMode==OFF for back-compat.
ENUM_AI_OS_MODE AOSEffectiveL2Mode()
  {
   if(InpAiKillSwitch)
      return AI_OS_OFF;
   if(InpAiOsMode != AI_OS_OFF)
      return InpAiOsMode;
   if(InpAOS_L2AI_Enable)
      return AI_OS_LIVE_WITHHOLD;
   if(InpAOS_L2AI_Shadow)
      return AI_OS_SHADOW;
   return AI_OS_OFF;
  }

//+------------------------------------------------------------------+
string AOSModeToString(const ENUM_AI_OS_MODE mode)
  {
   if(mode == AI_OS_LIVE_WITHHOLD) return "LIVE_WITHHOLD";
   if(mode == AI_OS_SHADOW) return "SHADOW";
   return "OFF";
  }

//+------------------------------------------------------------------+
void AOSInit()
  {
   ZeroMemory(g_aos);
   g_aos.fRec = 1.0;
   g_aos.life = AOS_LIFE_STABLE;
   g_aos.peakEquity = AccountInfoDouble(ACCOUNT_EQUITY);
   g_aos.ledgerHandle = INVALID_HANDLE;
   g_aos.haltReason = "";
   g_aos.lastL2Reason = "FIRE_OK";
   g_aos.inited = true;

   if(!InpAOS_Enable)
     {
      LogInfo("AOS disabled");
      return;
     }

   // Strip Tester "||meta" junk if present so preset compare works
   string pinWanted = InpAiModelSemver;
   const int pipe = StringFind(pinWanted, "||");
   if(pipe > 0)
      pinWanted = StringSubstr(pinWanted, 0, pipe);
   const string baked = AOSActiveL2Semver();
   if(StringCompare(pinWanted, baked) != 0 && AOSEffectiveL2Mode() != AI_OS_OFF)
      LogWarn(StringFormat(
                 "AOS model semver mismatch input=%s baked=%s — using baked coeffs for %s",
                 pinWanted, baked, _Symbol));

   if(InpAOS_Ledger)
     {
      const string fname = StringFormat("BMRG_AOS_ledger_%d.csv", (int)InpMagic);
      g_aos.ledgerHandle = FileOpen(fname, FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON, ',');
      if(g_aos.ledgerHandle != INVALID_HANDLE)
        {
         FileWrite(g_aos.ledgerHandle,
                   "t","side","layer","decision","reason",
                   "life","f_rec","w250_EF","w250_EN","ai_proba","ai_skip",
                   "model","halt","derisk","mode");
         LogInfo("AOS ledger -> COMMON\\Files\\" + fname);
        }
      else
         LogWarn("AOS ledger FileOpen failed err=" + IntegerToString(GetLastError()));
     }

   LogInfo(StringFormat(
              "AOS ON | L3=%d L4size=%d L2mode=%s kill=%d DDlim=%.1f W=%d model=%s sym=%s",
              (int)InpAOS_L3_Enable, (int)InpAOS_L4_SizeMod,
              AOSModeToString(AOSEffectiveL2Mode()), (int)InpAiKillSwitch,
              InpAOS_DD_Limit, InpAOS_W250, baked, _Symbol));
  }

//+------------------------------------------------------------------+
void AOSDeinit()
  {
   if(g_aos.ledgerHandle != INVALID_HANDLE)
     {
      FileClose(g_aos.ledgerHandle);
      g_aos.ledgerHandle = INVALID_HANDLE;
     }
  }

//+------------------------------------------------------------------+
void AOSLedger(const string side,
               const string layer,
               const string decision,
               const string reason)
  {
   if(!InpAOS_Enable || !InpAOS_Ledger || g_aos.ledgerHandle == INVALID_HANDLE)
      return;
   FileWrite(g_aos.ledgerHandle,
             TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES),
             side, layer, decision, reason,
             AOSLifeToString(g_aos.life),
             DoubleToString(g_aos.fRec, 2),
             DoubleToString(g_aos.w250EF, 2),
             DoubleToString(g_aos.w250EN, 4),
             DoubleToString(g_aos.lastAIProba, 4),
             (int)g_aos.lastAISkip,
             AOSActiveL2Semver(),
             (int)g_aos.haltL3,
             (int)g_aos.deriskL3,
             AOSModeToString(AOSEffectiveL2Mode()));
  }

//+------------------------------------------------------------------+
void AOSPushOutcome(const bool isWin)
  {
   if(!InpAOS_Enable)
      return;
   g_aos.ring[g_aos.ringHead] = isWin ? 1 : 0;
   g_aos.ringHead = (g_aos.ringHead + 1) % AOS_RING_MAX;
   if(g_aos.ringN < AOS_RING_MAX)
      g_aos.ringN++;
  }

//+------------------------------------------------------------------+
bool AOSWindowStats(const int w, double &wr, double &en, double &ef, double &m)
  {
   wr = 0.0; en = 0.0; ef = 0.0; m = 0.0;
   if(g_aos.ringN < w || w <= 0)
      return false;

   int tp = 0;
   for(int i = 0; i < w; i++)
     {
      const int idx = (g_aos.ringHead - 1 - i + AOS_RING_MAX * 2) % AOS_RING_MAX;
      if(g_aos.ring[idx] == 1)
         tp++;
     }
   wr = 100.0 * (double)tp / (double)w;
   const double bm = wr - InpAOS_BWR;
   en = (wr / 100.0) * (InpAOS_R + 1.0) - 1.0;
   ef = bm - InpAOS_Leak;
   const double p = wr / 100.0;
   m = 100.0 * 1.96 * MathSqrt(p * (1.0 - p) / (double)w);
   return true;
  }

//+------------------------------------------------------------------+
void AOSUpdatePeakAndDD()
  {
   const double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   if(eq > g_aos.peakEquity)
      g_aos.peakEquity = eq;
  }

//+------------------------------------------------------------------+
double AOSDrawdownPctFromPeak()
  {
   if(g_aos.peakEquity <= 0.0)
      return 0.0;
   const double eq = AccountInfoDouble(ACCOUNT_EQUITY);
   if(eq >= g_aos.peakEquity)
      return 0.0;
   return 100.0 * (g_aos.peakEquity - eq) / g_aos.peakEquity;
  }

//+------------------------------------------------------------------+
void AOSUpdateObserver()
  {
   if(!InpAOS_Enable)
      return;

   AOSUpdatePeakAndDD();

   double wr = 0, en = 0, ef = 0, m = 0;
   const bool have = AOSWindowStats(InpAOS_W250, wr, en, ef, m);
   if(have)
     {
      g_aos.w250WR = wr;
      g_aos.w250EN = en;
      g_aos.w250EF = ef;
     }

   // Lifecycle (v0)
   ENUM_AOS_LIFE life = AOS_LIFE_STABLE;
   if(have)
     {
      if(en <= 0.0)
         life = AOS_LIFE_BELOW;
      else if(ef <= 0.0)
         life = AOS_LIFE_NEAR;
      else if(ef <= m)
         life = AOS_LIFE_COMPRESSING;
      else
         life = AOS_LIFE_EXPANDING;
     }
   g_aos.life = life;

   double f = 1.0;
   switch(life)
     {
      case AOS_LIFE_EXPANDING:   f = 1.00; break;
      case AOS_LIFE_STABLE:      f = 0.75; break;
      case AOS_LIFE_COMPRESSING: f = 0.50; break;
      case AOS_LIFE_NEAR:        f = 0.25; break;
      case AOS_LIFE_BELOW:       f = 0.00; break;
     }

   // L3 MaxDD / derisk
   g_aos.haltL3 = false;
   g_aos.deriskL3 = false;
   g_aos.haltReason = "";
   if(InpAOS_L3_Enable)
     {
      const double dd = AOSDrawdownPctFromPeak();
      if(InpAOS_DD_Limit > 0.0 && dd >= InpAOS_DD_Limit)
        {
         g_aos.haltL3 = true;
         g_aos.haltReason = StringFormat("HALT_MAXDD dd=%.1f>=%.1f", dd, InpAOS_DD_Limit);
         f = 0.0;
        }
      else if(InpAOS_DD_Limit > 0.0 && dd >= 0.8 * InpAOS_DD_Limit)
        {
         g_aos.deriskL3 = true;
         f = MathMin(f, 0.5);
         g_aos.haltReason = StringFormat("DERISK_0.8_DD dd=%.1f", dd);
        }

      if(have && life == AOS_LIFE_BELOW)
        {
         g_aos.haltL3 = true;
         g_aos.haltReason = StringFormat("HALT_f0_BELOW_FRONTIER EN=%.4f EF=%.2f", en, ef);
         f = 0.0;
        }
     }

   if(!InpAOS_L4_SizeMod && !g_aos.haltL3)
      f = (g_aos.deriskL3 ? 0.5 : 1.0);

   g_aos.fRec = f;
  }

//+------------------------------------------------------------------+
double AOSScaleNum(const int i, const double raw, const bool aud)
  {
   const double s = aud ? AOS_L2AUD_NUM_SCALE[i] : AOS_L2INF_NUM_SCALE[i];
   const double mu = aud ? AOS_L2AUD_NUM_MEAN[i] : AOS_L2INF_NUM_MEAN[i];
   if(s == 0.0)
      return 0.0;
   return (raw - mu) / s;
  }

//+------------------------------------------------------------------+
double AOSPredictLoseProba(const ENUM_BMRG_SIDE side, const datetime t)
  {
   // Feature parity with train_l2shadow.py / train_l2_audusd.py
   const bool aud = AOSIsAudUsd();
   MqlDateTime dt;
   TimeToStruct(t, dt);
   const int hour = dt.hour;
   const int dow = dt.day_of_week; // 0=Sun .. 5=Fri
   const int month = dt.mon;
   const int wom = ((dt.day - 1) / 7) + 1;
   const int spread = (int)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD);
   const double spreadMed = aud ? AOS_L2AUD_SPREAD_MED : AOS_L2INF_SPREAD_MED;
   const int spreadHi = (spread >= (int)spreadMed) ? 1 : 0;
   const int isMon = (dow == 1) ? 1 : 0;
   const int isFri = (dow == 5) ? 1 : 0;
   const int sideBuy = (side == BMRG_SIDE_BUY) ? 1 : 0;
   // Match session_id: 12–16 LON_NY · 17–19 NY
   const bool sessLonNy = (hour >= 12 && hour < 17);
   const bool sessNy = (hour >= 17 && hour < 20);

   const int nFeat = aud ? AOS_L2AUD_N_FEAT : AOS_L2INF_N_FEAT;
   double x[];
   ArrayResize(x, nFeat);
   ArrayInitialize(x, 0.0);

   if(sessLonNy) x[0] = 1.0;
   if(sessNy) x[1] = 1.0;
   if(sideBuy == 1) x[2] = 1.0; else x[3] = 1.0;
   if(dow == 5) x[4] = 1.0;
   else if(dow == 1) x[5] = 1.0;
   else if(dow == 4) x[6] = 1.0;
   else if(dow == 3) x[7] = 1.0;

   x[8]  = AOSScaleNum(0, (double)hour, aud);
   x[9]  = AOSScaleNum(1, (double)spread, aud);
   x[10] = AOSScaleNum(2, (double)month, aud);
   x[11] = AOSScaleNum(3, (double)wom, aud);
   x[12] = AOSScaleNum(4, (double)isMon, aud);
   x[13] = AOSScaleNum(5, (double)isFri, aud);
   x[14] = AOSScaleNum(6, (double)sideBuy, aud);
   x[15] = AOSScaleNum(7, (double)spreadHi, aud);

   double z = aud ? AOS_L2AUD_INTERCEPT : AOS_L2INF_INTERCEPT;
   for(int i = 0; i < nFeat; i++)
      z += (aud ? AOS_L2AUD_COEF[i] : AOS_L2INF_COEF[i]) * x[i];

   if(z > 35.0) return 1.0;
   if(z < -35.0) return 0.0;
   return 1.0 / (1.0 + MathExp(-z));
  }

//+------------------------------------------------------------------+
double AOSLotMultiplier()
  {
   if(!InpAOS_Enable)
      return 1.0;
   if(g_aos.haltL3)
      return 0.0;
   if(!InpAOS_L4_SizeMod && !g_aos.deriskL3)
      return 1.0;
   return MathMax(0.0, MathMin(1.0, g_aos.fRec));
  }

//+------------------------------------------------------------------+
bool AOSAllowEntry(const ENUM_BMRG_SIDE side, string &reason)
  {
   reason = "";
   g_aos.lastAISkip = false;
   g_aos.lastAIProba = 0.0;
   g_aos.lastL2Reason = "FIRE_OK";

   if(!InpAOS_Enable)
      return true;

   AOSUpdateObserver();

   // L3 command — outranks L2
   if(InpAOS_L3_Enable && g_aos.haltL3)
     {
      reason = "AOS L3 " + g_aos.haltReason;
      AOSLedger(SideToString(side), "L3", "HALT_SKIP", reason);
      return false;
     }

   if(AOSLotMultiplier() <= 0.0)
     {
      reason = "AOS f_rec=0 (" + AOSLifeToString(g_aos.life) + ")";
      AOSLedger(SideToString(side), "L4", "SIZE_ZERO", reason);
      return false;
     }

   // L2 mode: kill-switch / OFF → no intelligence (Apple det still needs mode≠OFF)
   const ENUM_AI_OS_MODE l2mode = AOSEffectiveL2Mode();
   if(l2mode == AI_OS_OFF)
     {
      AOSLedger(SideToString(side), "L2", "FIRE", "L2_OFF");
      return true;
     }

   // --- UK100 path: L2det only (never run EUR/AUD L2 AI coeffs on UK100) ---
   if(AOSIsUk100Symbol())
     {
      string detReason = "";
      if(AOSUkL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- Apple M5 path: M5-native L2det only (never M15 Thu/18 · never EUR/AUD AI) ---
   if(AOSIsAppleSymbol() && Period() == PERIOD_M5 && InpAOS_AAPL_M5_L2detEnable)
     {
      string detReason = "";
      if(AOSAppleM5L2detShouldSkip(TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- Apple M15 path: L2det only (never run EUR/AUD L2 AI coeffs on Apple) ---
   if(AOSIsAppleSymbol())
     {
      string detReason = "";
      if(AOSAppleL2detShouldSkip(TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- EURUSD M15 research OS: L2det only when enabled (never INF coeffs) ---
   if(AOSIsEurUsdSymbol() && InpAOS_EUR_L2detEnable)
     {
      string detReason = "";
      if(AOSEurL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- AUDUSD M15 research OS: L2det only when enabled (never live M5 AI pin) ---
   if(AOSIsAudUsd() && InpAOS_AUD_L2detEnable)
     {
      string detReason = "";
      if(AOSAudL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- DE40/DE30 M5 research OS: L2det v1b (before M15 map) ---
   if(AOSIsDe40Symbol() && Period() == PERIOD_M5 && InpAOS_DE_M5_L2detEnable)
     {
      string detReason = "";
      if(AOSDeM5L2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- DE40/DE30 M15 research OS: L2det only when enabled (not on M5) ---
   if(AOSIsDe40Symbol() && Period() != PERIOD_M5 && InpAOS_DE_L2detEnable)
     {
      string detReason = "";
      if(AOSDeL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- JP225/JPN225 M5 research OS: L2det v1c (before M15 May∨Jul map) ---
   if(AOSIsJp225Symbol() && Period() == PERIOD_M5 && InpAOS_JP_M5_L2detEnable)
     {
      string detReason = "";
      if(AOSJpM5L2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- JP225/JPN225 M15 research OS: L2det only when enabled (not on M5) ---
   if(AOSIsJp225Symbol() && Period() != PERIOD_M5 && InpAOS_JP_L2detEnable)
     {
      string detReason = "";
      if(AOSJpL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- USDJPY M15 research OS: L2det only when enabled ---
   if(AOSIsUsdJpySymbol() && InpAOS_USDJPY_L2detEnable)
     {
      string detReason = "";
      if(AOSUsdJpyL2detShouldSkip(side, TimeCurrent(), detReason))
        {
         g_aos.lastL2Reason = detReason;
         g_aos.lastAISkip = true;
         if(l2mode == AI_OS_LIVE_WITHHOLD)
           {
            reason = "AOS " + detReason;
            AOSLedger(SideToString(side), "L2DET", "SKIP", detReason);
            return false;
           }
         LogInfo("AOS SHADOW skip " + detReason);
         AOSLedger(SideToString(side), "L2DET", "SHADOW_SKIP", detReason);
        }
      else
        {
         g_aos.lastL2Reason = "FIRE_OK";
         AOSLedger(SideToString(side), "L2DET", "FIRE", "FIRE_OK");
        }
      return true;
     }

   // --- FX path: L2 AI (INF / AUD) — permit/withhold only ---
   const double proba = AOSPredictLoseProba(side, TimeCurrent());
   g_aos.lastAIProba = proba;
   const bool aud = AOSIsAudUsd();
   const double thr = aud ? AOS_L2AUD_THR : AOS_L2INF_THR;
   const double band = aud ? AOS_L2AUD_UNCERTAIN : AOS_L2INF_UNCERTAIN;
   // Policy: WOULD_SKIP only if p >= thr+band; near thr → ALLOW_UNCERTAIN (fire)
   const bool wantSkip = (proba >= (thr + band));
   const bool uncertain = (!wantSkip && proba >= (thr - band));
   g_aos.lastAISkip = wantSkip;

   if(wantSkip)
     {
      g_aos.lastL2Reason = StringFormat("L2%s WOULD_SKIP p=%.3f thr=%.3f",
                                        aud ? "AUD" : "INF", proba, thr);
      if(l2mode == AI_OS_LIVE_WITHHOLD)
        {
         reason = "AOS " + g_aos.lastL2Reason;
         AOSLedger(SideToString(side), "L2AI", "SKIP", g_aos.lastL2Reason);
         return false;
        }
      // SHADOW: log only, engine still fires
      LogInfo("AOS SHADOW skip " + g_aos.lastL2Reason);
      AOSLedger(SideToString(side), "L2AI", "SHADOW_SKIP", g_aos.lastL2Reason);
     }
   else if(uncertain)
     {
      g_aos.lastL2Reason = StringFormat("L2%s ALLOW_UNCERTAIN p=%.3f",
                                        aud ? "AUD" : "INF", proba);
      AOSLedger(SideToString(side), "L2", "ALLOW_UNCERTAIN", g_aos.lastL2Reason);
     }
   else
     {
      AOSLedger(SideToString(side), "L2", "FIRE", "FIRE_OK");
     }

   return true;
  }

//+------------------------------------------------------------------+
void AOSOnClosedDeal(const double profit)
  {
   if(!InpAOS_Enable)
      return;
   // Geometry RR≈1: profit>0 ≈ TP, profit<0 ≈ SL
   if(profit == 0.0)
      return;
   AOSPushOutcome(profit > 0.0);
   AOSUpdateObserver();
   LogInfo(StringFormat(
              "AOS close %s | n=%d life=%s f=%.2f W250 EF=%.2f EN=%.3f halt=%d",
              (profit > 0.0 ? "TP" : "SL"),
              g_aos.ringN,
              AOSLifeToString(g_aos.life),
              g_aos.fRec,
              g_aos.w250EF,
              g_aos.w250EN,
              (int)g_aos.haltL3));
  }

//+------------------------------------------------------------------+
string AOSStatusLine()
  {
   if(!InpAOS_Enable)
      return "AOS off";
   return StringFormat("AOS %s f=%.2f EF%.1f halt=%d ai=%.2f/%s",
                       AOSLifeToString(g_aos.life),
                       g_aos.fRec,
                       g_aos.w250EF,
                       (int)g_aos.haltL3,
                       g_aos.lastAIProba,
                       AOSModeToString(AOSEffectiveL2Mode()));
  }

#endif // BMRG_AOS_MQH
