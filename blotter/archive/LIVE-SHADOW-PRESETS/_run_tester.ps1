# Headless MT5 Strategy Tester: LIVE-SHADOW presets, 2026.01.01 -> 2026.09.30, every tick, $500, 1:500.
# Requires the local terminal to be closed (one instance per data folder).
# -Prefix LIVE-SHADOW (default) or LIVE-CURRENT (exact live inputs, LIVE_WITHHOLD baseline).
param([string]$Prefix = "LIVE-SHADOW")
$ErrorActionPreference = "Stop"
$term   = "C:\Program Files\MetaTrader 5\terminal64.exe"
$data   = "C:\Users\emili\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075"
$iniDir = Join-Path $PSScriptRoot "tester_ini"
New-Item -ItemType Directory -Force $iniDir | Out-Null
New-Item -ItemType Directory -Force (Join-Path $data "Tester\reports") | Out-Null

$runs = @(
  @{ Set = "$Prefix`_EURUSD_M5.set";  Symbol = "EURUSD"; Period = "M5"  },
  @{ Set = "$Prefix`_AUDUSD_M5.set";  Symbol = "AUDUSD"; Period = "M5"  },
  @{ Set = "$Prefix`_Apple_M5.set";   Symbol = "Apple";  Period = "M5"  },
  @{ Set = "$Prefix`_UK100_M5.set";   Symbol = "UK100";  Period = "M5"  },
  @{ Set = "$Prefix`_JPN225_M5.set";  Symbol = "JPN225"; Period = "M5"  },
  @{ Set = "$Prefix`_DE30_M5.set";    Symbol = "DE30";   Period = "M5"  },
  @{ Set = "$Prefix`_USDJPY_M15.set"; Symbol = "USDJPY"; Period = "M15" }
)

foreach ($r in $runs) {
  $name = [IO.Path]::GetFileNameWithoutExtension($r.Set)
  $ini  = Join-Path $iniDir "$name.ini"
  $sub  = if (Test-Path (Join-Path $data "MQL5\Profiles\Tester\BMRG\live\$($r.Set)")) { "BMRG\live" } else { "BMRG" }
  @"
[Tester]
Expert=BMRG\BMRG.ex5
ExpertParameters=$sub\$($r.Set)
Symbol=$($r.Symbol)
Period=$($r.Period)
Model=0
ExecutionMode=0
Optimization=0
FromDate=2026.01.01
ToDate=2026.09.30
ForwardMode=0
Deposit=500
Currency=USD
ProfitInPips=0
Leverage=500
UseLocal=1
UseRemote=0
UseCloud=0
Visual=0
Report=Tester\reports\$name
ReplaceReport=1
ShutdownTerminal=1
"@ | Set-Content -Encoding ASCII $ini

  $t0 = Get-Date
  Write-Output "$(Get-Date -Format HH:mm:ss) START $name"
  Start-Process -FilePath $term -ArgumentList "/config:`"$ini`"" -Wait
  Write-Output ("$(Get-Date -Format HH:mm:ss) DONE  $name in {0:N0}s" -f ((Get-Date) - $t0).TotalSeconds)
}
Write-Output "ALL DONE"

