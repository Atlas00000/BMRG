@echo off
REM Windows shim when GNU make is unavailable. Usage: make.bat test
setlocal
cd /d "%~dp0"
if "%~1"=="" goto help
if /I "%~1"=="up" (
  docker-compose up -d postgres redis
  goto :eof
)
if /I "%~1"=="down" (
  docker-compose down
  goto :eof
)
if /I "%~1"=="ingest" (
  python src/ingest/run_p2_e2e.py
  goto :eof
)
if /I "%~1"=="features" (
  python src/features/build_l1_tape.py
  goto :eof
)
if /I "%~1"=="train" (
  python src/train/train_l2shadow.py
  goto :eof
)
if /I "%~1"=="score" (
  python -c "import json,sys; from pathlib import Path; sys.path[:0]=['src/score','src/ingest']; from health import score_pack_dir; r=score_pack_dir(Path('fixtures/blotter/harvest_long_v1')); print(json.dumps({'verdict':r['verdict'],'ef':r['health_vector']['ef_pp'],'n':r['health_vector']['n']},indent=2))"
  goto :eof
)
if /I "%~1"=="eval" (
  python src/eval/run_p4b_e2e.py
  goto :eof
)
if /I "%~1"=="report" (
  python -c "import pathlib; p=pathlib.Path('artefacts/reports/LATEST_EVAL.json'); print(p.read_text(encoding='utf-8')[:5000] if p.exists() else 'MISSING')"
  goto :eof
)
if /I "%~1"=="test" (
  python -m pytest src/ingest/test_p1_contract.py src/ingest/test_p2_ingest.py src/features/test_p3_features.py src/train/test_p4a_train.py src/eval/test_p4b_eval.py src/obs/test_p5a_obs.py src/score/test_fx.py src/jobqueue/test_queue.py src/test_p5b_suite.py -q --tb=line
  goto :eof
)
if /I "%~1"=="queue-demo" (
  docker-compose up -d postgres redis
  python src/jobqueue/enqueue.py --job p4_eval
  python src/jobqueue/worker.py --once --timeout 60
  goto :eof
)
if /I "%~1"=="smoke" (
  docker-compose up -d postgres redis
  python src/obs/run_p5a_e2e.py
  python src/jobqueue/run_p5b_e2e.py
  goto :eof
)
:help
echo Targets: up down ingest features train score eval report test queue-demo smoke
endlocal
