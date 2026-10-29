//+------------------------------------------------------------------+
//| Config.mqh — inputs: signal, filters, risk, exposure, containment  |
//+------------------------------------------------------------------+
#ifndef BMRG_CONFIG_MQH
#define BMRG_CONFIG_MQH

enum ENUM_BMRG_LOT_MODE
  {
   BMRG_LOT_FIXED = 0,          // Fixed lot
   BMRG_LOT_RISK_PCT = 1        // Risk % of equity (requires SL)
  };

enum ENUM_BMRG_EQUITY_BASE
  {
   BMRG_EQ_BALANCE = 0,
   BMRG_EQ_EQUITY  = 1
  };

input group "=== Indicators ==="
input int      InpBBPeriod          = 20;       // BB period
input double   InpBBDev             = 2.0;      // BB deviation (σ)
input int      InpATRPeriod         = 14;       // ATR period (regime)

input group "=== Grid ==="
input int      InpMaxLevels         = 1;        // Max grid levels per side
input double   InpLevelStepSigma    = 0.5;      // Extra σ between levels

input group "=== Fade confirm (WR gate) ==="
input bool     InpUseFadeConfirm    = false;    // Setup at band → enter only on reclaim
input int      InpFadeConfirmMaxBars = 3;       // Bars to wait for reclaim; then expire
input bool     InpFadeRequireInsideMid = true;  // Confirm close must stay on setup side of mid

input group "=== Lot / risk % ==="
input ENUM_BMRG_LOT_MODE InpLotMode = BMRG_LOT_FIXED; // Lot mode
input double   InpLot               = 0.01;     // Fixed lot (if Fixed mode)
input double   InpRiskPercent       = 0.5;      // Risk % of account per entry
input ENUM_BMRG_EQUITY_BASE InpRiskBase = BMRG_EQ_EQUITY; // Risk base
input double   InpMaxLot            = 1.0;      // Hard cap lot
input double   InpMinLotOverride    = 0.0;      // Min lot override; 0 = symbol min

input group "=== Stops & friction ==="
input int      InpSL_Points         = 200;      // SL points (0=off; required for Risk%)
input int      InpTP_Points         = 0;        // TP points; 0 = off
input int      InpMaxSpread         = 30;       // Max spread points; 0 = off
input ulong    InpSlippage          = 10;       // Slippage points
input int      InpCooldownBars      = 1;        // Bars between new entries

input group "=== Exposure & account gates ==="
input int      InpMaxEntries        = 1;        // Max open entries (basket)
input double   InpMaxExposurePct    = 20.0;     // Max margin exposure % of equity; 0=off
input double   InpMinFreeMarginPct  = 50.0;     // Min free margin % of equity; 0=off
input double   InpMaxBasketLossPct  = 3.0;      // Max floating basket loss %; 0=off
input double   InpEquityHaltPct     = 10.0;     // Halt new entries if DD% from start; 0=off
input double   InpMaxDailyLossPct   = 3.0;      // Max daily loss % from day start; 0=off
input int      InpMaxDailyEntries   = 20;       // Max new entries per day; 0=off

input group "=== Time filter (server) ==="
input bool     InpUseTimeFilter     = false;    // Enable session time filter
input int      InpStartHour         = 8;        // Session start hour
input int      InpStartMinute       = 0;        // Session start minute
input int      InpEndHour           = 20;       // Session end hour
input int      InpEndMinute         = 0;        // Session end minute
input bool     InpTradeMon          = true;     // Trade Monday
input bool     InpTradeTue          = true;     // Trade Tuesday
input bool     InpTradeWed          = true;     // Trade Wednesday
input bool     InpTradeThu          = true;     // Trade Thursday
input bool     InpTradeFri          = true;     // Trade Friday
input bool     InpTradeSat          = false;    // Trade Saturday
input bool     InpTradeSun          = false;    // Trade Sunday

input group "=== Regime gates ==="
input bool     InpUseATRRegime      = false;    // Filter by ATR points range
input double   InpATRMinPoints      = 0.0;      // Min ATR (points); 0=off
input double   InpATRMaxPoints      = 0.0;      // Max ATR (points); 0=off
input bool     InpUseBBWidthRegime  = false;    // Filter by BB width %
input double   InpBBWidthMinPct     = 0.0;      // Min (upper-lower)/mid*100; 0=off
input double   InpBBWidthMaxPct     = 0.0;      // Max BB width %; 0=off

input group "=== Failure containment ==="
input int      InpMaxOrderFails     = 3;        // Consecutive order fails → pause; 0=off
input int      InpMaxLossStreak     = 3;        // Consecutive losing closes → pause; 0=off
input int      InpFailPauseBars     = 12;       // Bars to pause after fail/loss trip
input bool     InpCloseOnDailyLoss  = false;    // Flatten basket if daily loss hit
input bool     InpBlockBusyTradeCtx = true;     // Block if trade context busy

input group "=== Permissions ==="
input bool     InpAllowBuy          = true;     // Allow long entries
input bool     InpAllowSell         = true;     // Allow short entries
input long     InpMagic             = 26092101; // Magic number

input group "=== Logging ==="
input bool     InpLogToComment      = true;     // Chart Comment panel
input bool     InpLogGateBlocks     = true;     // Log every gate block

input group "=== AOS (AI OS) ==="
input bool     InpAOS_Enable        = false;    // Master enable AOS overlay
input bool     InpAOS_L3_Enable     = true;     // L3 MaxDD / Below-frontier halt
input bool     InpAOS_L4_SizeMod    = true;     // L4 lifecycle → lot multiplier
// L2 mode (INF LIVE_WITHHOLD): OFF=no L2 · SHADOW=log only · LIVE_WITHHOLD=block order on WOULD_SKIP
enum ENUM_AI_OS_MODE
  {
   AI_OS_OFF = 0,              // No L2 intelligence
   AI_OS_SHADOW = 1,           // Log would-skip; engine still fires
   AI_OS_LIVE_WITHHOLD = 2     // Withhold new entries on L2 WOULD_SKIP
  };
input ENUM_AI_OS_MODE InpAiOsMode   = AI_OS_OFF; // INF L2 attach mode
input string   InpAiModelSemver     = "L2skip_inf_p92_20260927_223519"; // Must match baked INF model
input bool     InpAiKillSwitch      = false;    // Force L2 OFF (one-click rollback)
input bool     InpAOS_L2AI_Enable   = false;    // DEPRECATED: use InpAiOsMode=LIVE_WITHHOLD
input bool     InpAOS_L2AI_Shadow   = true;     // DEPRECATED: use InpAiOsMode=SHADOW
input double   InpAOS_DD_Limit      = 25.0;     // L3 MaxDD % from peak equity
input double   InpAOS_BWR           = 50.0;     // Break-even WR % (R=1 → 50)
input double   InpAOS_Leak          = 2.2;      // Leak pp for EF
input double   InpAOS_R             = 1.0;      // Designed R for E_N
input int      InpAOS_W250          = 250;      // Primary rolling window for L4/L3 observer
input bool     InpAOS_L3_BelowDualWindow = true; // BELOW halt needs W20 EN≤0 AND W15 EF≤0 (signed P3)
input int      InpAOS_L3_BelowConfirmN   = 2;    // Consecutive BELOW *closes* before hard halt (1=legacy immediate)
input bool     InpAOS_L3_BelowSoftDerisk = true; // While confirming BELOW: f≤0.25 derisk instead of f=0
input int      InpAOS_L3_BelowHaltMaxBars = 500; // Bars after hard BELOW halt → probe unlatch (0=off). M5≈2 sessions
input bool     InpAOS_Ledger        = true;     // Write AOS ledger CSV (COMMON\\Files)
// Apple M15 L2det (only when Apple/AAPL and NOT M5 — see AOS_L2det_aapl.mqh)
input bool     InpAOS_AAPL_L2detEnable = false; // Enable Apple M15 Thu/hour-18 L2det map
input bool     InpAOS_AAPL_SkipThu     = true;  // Skip Thursday entries (Apple M15)
input bool     InpAOS_AAPL_SkipHour18  = true;  // Skip hour==18 server time (Apple M15)
// Apple M5 L2det v1b (research OS — do NOT reuse M15 Thu/18 map)
input bool     InpAOS_AAPL_M5_L2detEnable    = false; // Enable Apple M5 Jul∨Wed map
input bool     InpAOS_AAPL_M5_SkipJul        = true;  // Skip month==Jul (ARM)
input bool     InpAOS_AAPL_M5_SkipWed        = true;  // Skip DOW==Wed (ARM)
input bool     InpAOS_AAPL_M5_SkipHour18     = false; // Optional H18 (HOLD — May FP)
input bool     InpAOS_AAPL_M5_SkipHighSpread = false; // Optional spread≥thr (HOLD)
input bool     InpAOS_AAPL_M5_SkipH1         = false; // Optional Jan–Apr (YTD HOLD)
input int      InpAOS_AAPL_M5_SpreadThr      = 30;    // High-spread threshold (pts)
// UK100 L2det v1b (only when symbol is UK100/FTSE — see AOS_L2det_uk.mqh)
input bool     InpAOS_UK_L2detEnable   = false; // Enable UK100 Thu / BUY∧nearATR map
input bool     InpAOS_UK_SkipThu       = true;  // Skip Thursday entries (UK100)
input bool     InpAOS_UK_SkipBuyNearAtr = true; // Skip BUY when ATR ≥ frac×cap
input bool     InpAOS_UK_SkipJul       = false; // Optional Jul calendar seed (tip only)
input double   InpAOS_UK_AtrCapPoints  = 1470.0;// ATR cap reference (same as InpATRMaxPoints)
input double   InpAOS_UK_NearAtrFrac   = 0.9;   // near_atr threshold = frac × atrCap
// EURUSD M15 L2det v1b (research OS only — do NOT arm on M5 Harvest live)
input bool     InpAOS_EUR_L2detEnable   = false; // Enable EURUSD M15 Thu / BUY∧nearATR map
input bool     InpAOS_EUR_SkipThu       = true;  // Skip Thursday entries (EURUSD M15)
input bool     InpAOS_EUR_SkipBuyNearAtr = true; // Skip BUY when ATR ≥ frac×cap
input double   InpAOS_EUR_AtrCapPoints  = 74.0;  // ATR cap reference (InpATRMaxPoints M15)
input double   InpAOS_EUR_NearAtrFrac   = 0.9;   // near_atr threshold = frac × atrCap
// AUDUSD M15 L2det v1 (research OS only — do NOT arm on live M5 SCALE 8230931)
input bool     InpAOS_AUD_L2detEnable   = false; // Enable AUDUSD M15 BUY∧May map
input bool     InpAOS_AUD_SkipBuyMay    = true;  // Skip BUY when month==May (preferred)
input bool     InpAOS_AUD_SkipBuyThu    = false; // Optional alt: Skip BUY when DOW==Thu
// DE40/DE30 M15 L2det v1 (research OS / DE40stack only — expansion sleeve)
input bool     InpAOS_DE_L2detEnable    = false; // Enable DE40 BUY∧nearATR map
input bool     InpAOS_DE_SkipBuyNearAtr = true;  // Skip BUY when ATR ≥ frac×cap
input bool     InpAOS_DE_SkipH13        = false; // Optional H13 (HOLD — Aug FP; off)
input double   InpAOS_DE_AtrCapPoints   = 4070.0;// ATR cap reference (InpATRMaxPoints)
input double   InpAOS_DE_NearAtrFrac    = 0.9;   // near_atr threshold = frac × atrCap
// DE40/DE30 M5 L2det v1b (research OS / DE40M5stack — do NOT reuse M15 map)
input bool     InpAOS_DE_M5_L2detEnable     = false; // Enable DE40 M5 BUY∧H14/16∨BUY∧Oct
input bool     InpAOS_DE_M5_SkipBuyH14_16   = true;  // Skip BUY when hour∈{14,16}
input bool     InpAOS_DE_M5_SkipBuyOct      = true;  // Skip BUY when month==Oct
input bool     InpAOS_DE_M5_SkipH14_16All   = false; // Optional: all sides H14/16 (SELL FP)
input bool     InpAOS_DE_M5_SkipOctAll      = false; // Optional: Oct all sides (SELL FP)
// JP225/JPN225 M15 L2det v1 (research OS / JPN225stack only — expansion sleeve)
input bool     InpAOS_JP_L2detEnable    = false; // Enable JP225 May∨Jul map (M15 only)
input bool     InpAOS_JP_SkipMay        = true;  // Skip month==May
input bool     InpAOS_JP_SkipJul        = true;  // Skip month==Jul
input bool     InpAOS_JP_SkipWed        = false; // Optional Wed (HOLD — Aug FP; off)
// JP225/JPN225 M5 L2det v1c (research OS / JPN225_5m_stack — do NOT reuse M15 May∨Jul)
input bool     InpAOS_JP_M5_L2detEnable       = false; // Enable M5 BUY∧MATCH∨BUY∧H09|13|16
input bool     InpAOS_JP_M5_SkipBuyMatch      = true;  // Skip BUY when Aug/Sep MATCH
input bool     InpAOS_JP_M5_SkipBuyH09_13_16  = true;  // Skip BUY when hour∈{9,13,16}
input bool     InpAOS_JP_M5_SkipMatchAll      = false; // Optional: MATCH all sides (SELL FP)
// USDJPY M15 L2det v1c (research OS / USDJPYstack only — expansion sleeve)
input bool     InpAOS_USDJPY_L2detEnable  = false; // Enable USDJPY nearATR∨H16 map
input bool     InpAOS_USDJPY_SkipNearAtr  = true;  // Skip when ATR ≥ frac×cap
input bool     InpAOS_USDJPY_SkipH16      = true;  // Skip hour==16
input bool     InpAOS_USDJPY_SkipJul      = false; // Optional Jul (HOLD — protect FP; off)
input double   InpAOS_USDJPY_AtrCapPoints = 70.0;  // ATR cap reference (InpATRMaxPoints)
input double   InpAOS_USDJPY_NearAtrFrac  = 0.9;   // near_atr threshold = frac × atrCap

//+------------------------------------------------------------------+
bool ConfigIsHedgingAccount()
  {
   return (AccountInfoInteger(ACCOUNT_MARGIN_MODE) == ACCOUNT_MARGIN_MODE_RETAIL_HEDGING);
  }

//+------------------------------------------------------------------+
// Trading gate: true once the connected account is confirmed hedging.
// Rechecked every tick until it passes, so a pre-sync read cannot
// permanently disable the EA; a real netting account never trades.
bool g_cfgAccountModeOK     = false;
bool g_cfgAccountModeLogged = false;

bool ConfigAccountModeOK()
  {
   if(g_cfgAccountModeOK)
      return true;
   if(!TerminalInfoInteger(TERMINAL_CONNECTED) || AccountInfoInteger(ACCOUNT_LOGIN) == 0)
      return false;
   if(!ConfigIsHedgingAccount())
     {
      if(!g_cfgAccountModeLogged)
        {
         Print("[BMRG][WARN] Trading paused: account not reported as hedging (netting unsupported) — rechecking each tick");
         g_cfgAccountModeLogged = true;
        }
      return false;
     }
   g_cfgAccountModeOK = true;
   Print("[BMRG][INFO] Account check OK: hedging");
   return true;
  }

//+------------------------------------------------------------------+
// Account margin mode is not checked here: in OnInit after a VPS restart the
// account may not be synchronized yet and reports a non-hedging default.
// See ConfigAccountModeOK(), called from OnTick.
bool ConfigValidate(string &reason)
  {
   reason = "";

   if(InpBBPeriod < 2) { reason = "BBPeriod must be >= 2"; return false; }
   if(InpBBDev <= 0.0) { reason = "BBDev must be > 0"; return false; }
   if(InpATRPeriod < 1) { reason = "ATRPeriod must be >= 1"; return false; }
   if(InpMaxLevels < 1) { reason = "MaxLevels must be >= 1"; return false; }
   if(InpLevelStepSigma <= 0.0) { reason = "LevelStepSigma must be > 0"; return false; }
   if(InpFadeConfirmMaxBars < 1) { reason = "FadeConfirmMaxBars must be >= 1"; return false; }
   if(InpLot <= 0.0) { reason = "Lot must be > 0"; return false; }
   if(InpRiskPercent < 0.0 || InpRiskPercent > 100.0)
     { reason = "RiskPercent must be 0..100"; return false; }
   if(InpLotMode == BMRG_LOT_RISK_PCT && InpSL_Points <= 0)
     { reason = "Risk% mode requires SL_Points > 0"; return false; }
   if(InpMaxLot <= 0.0) { reason = "MaxLot must be > 0"; return false; }
   if(InpMinLotOverride < 0.0) { reason = "MinLotOverride must be >= 0"; return false; }
   if(InpMaxEntries < 1) { reason = "MaxEntries must be >= 1"; return false; }
   if(InpMaxSpread < 0 || InpCooldownBars < 0 || InpSL_Points < 0 || InpTP_Points < 0)
     { reason = "Spread/Cooldown/SL/TP must be >= 0"; return false; }
   // Geometry mode: never arm TP < SL (designed RR must be >= 1.0)
   if(InpTP_Points > 0 && InpSL_Points > 0 && InpTP_Points < InpSL_Points)
     { reason = "TP_Points must be >= SL_Points when TP is on"; return false; }
   if(InpMaxExposurePct < 0.0 || InpMinFreeMarginPct < 0.0 ||
      InpMaxBasketLossPct < 0.0 || InpEquityHaltPct < 0.0 || InpMaxDailyLossPct < 0.0)
     { reason = "Exposure/halt/daily % must be >= 0"; return false; }
   if(InpMaxDailyEntries < 0) { reason = "MaxDailyEntries must be >= 0"; return false; }
   if(InpStartHour < 0 || InpStartHour > 23 || InpEndHour < 0 || InpEndHour > 23 ||
      InpStartMinute < 0 || InpStartMinute > 59 || InpEndMinute < 0 || InpEndMinute > 59)
     { reason = "Session time out of range"; return false; }
   if(InpATRMinPoints < 0.0 || InpATRMaxPoints < 0.0)
     { reason = "ATR min/max must be >= 0"; return false; }
   if(InpBBWidthMinPct < 0.0 || InpBBWidthMaxPct < 0.0)
     { reason = "BB width min/max must be >= 0"; return false; }
   if(InpMaxOrderFails < 0 || InpMaxLossStreak < 0 || InpFailPauseBars < 0)
     { reason = "Failure containment values must be >= 0"; return false; }
   if(!InpAllowBuy && !InpAllowSell)
     { reason = "AllowBuy and AllowSell cannot both be false"; return false; }
   if(InpMagic == 0) { reason = "Magic must be non-zero"; return false; }
   if(InpAOS_DD_Limit < 0.0) { reason = "AOS DD_Limit must be >= 0"; return false; }
   if(InpAOS_W250 < 50) { reason = "AOS W250 must be >= 50"; return false; }
   if(InpAOS_BWR <= 0.0 || InpAOS_BWR >= 100.0) { reason = "AOS BWR must be in (0,100)"; return false; }
   if(InpAOS_R <= 0.0) { reason = "AOS R must be > 0"; return false; }
   if(InpAOS_Leak < 0.0) { reason = "AOS Leak must be >= 0"; return false; }

   return true;
  }

#endif // BMRG_CONFIG_MQH
