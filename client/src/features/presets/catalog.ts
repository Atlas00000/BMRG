export const PRESET_CATALOG = [
  {
    role: 'Harvest champion',
    file: 'EDX-P2-T04_SL300_TP300_RR1_champFilters_G0_long.set',
    magic: 8210204,
    stack: 'Engine only',
  },
  {
    role: 'aistack paper',
    file: 'aistack.set',
    magic: 8399001,
    stack: 'STAY_PAPER',
  },
  {
    role: 'INF LIVE_WITHHOLD',
    file: 'INF-LIVE_WITHHOLD_Harvest_long.set',
    magic: 8210204,
    stack: 'AOS · InpAiOsMode=2',
  },
  {
    role: 'INF LIVE_WITHHOLD ddl30',
    file: 'INF-LIVE_WITHHOLD_Harvest_long_ddl30.set',
    magic: 8210204,
    stack: 'AOS · daily loss 30%',
  },
  {
    role: 'INF export-only',
    file: 'EXP-P7-T03_export_Harvest_long.set',
    magic: 8210205,
    stack: 'Engine export',
  },
  {
    role: 'Growth secondary',
    file: 'EDX-P4-T01_champion_T05_currency_G0_long.set',
    magic: 8210401,
    stack: 'Not OS default',
  },
] as const;
