# INF agent commands — no live forward-test. See AGENT_PATHS.md · BOX.md
COMPOSE ?= docker-compose
PHASE ?= P2
PYTHON ?= python

.PHONY: up down build smoke replay report test obs \
	ingest features train score eval queue-demo worker-once help

help:
	@echo "Targets: up down ingest features train score eval report test queue-demo smoke"

up:
	$(COMPOSE) up -d postgres redis

down:
	$(COMPOSE) down

build:
	$(COMPOSE) --profile jobs build

ingest:
	$(PYTHON) src/ingest/run_p2_e2e.py

features:
	$(PYTHON) src/features/build_l1_tape.py

train:
	$(PYTHON) src/train/train_l2shadow.py

score:
	$(PYTHON) -c "import json,sys; from pathlib import Path; sys.path[:0]=['src/score','src/ingest']; from health import score_pack_dir; r=score_pack_dir(Path('fixtures/blotter/harvest_long_v1')); print(json.dumps({'verdict':r['verdict'],'ef':r['health_vector']['ef_pp'],'n':r['health_vector']['n']},indent=2))"

eval:
	$(PYTHON) src/eval/run_p4b_e2e.py

obs:
	$(PYTHON) src/obs/run_p5a_e2e.py

smoke: up
	$(PYTHON) src/obs/run_p5a_e2e.py
	$(PYTHON) src/jobqueue/run_p5b_e2e.py

replay:
ifeq ($(PHASE),P2)
	$(PYTHON) src/ingest/run_p2_e2e.py
else ifeq ($(PHASE),P4b)
	$(PYTHON) src/eval/run_p4b_e2e.py
else ifeq ($(PHASE),P5a)
	$(PYTHON) src/obs/run_p5a_e2e.py
else ifeq ($(PHASE),P5b)
	$(PYTHON) src/jobqueue/run_p5b_e2e.py
else
	@echo "Unknown PHASE=$(PHASE); use P2|P4b|P5a|P5b" && exit 1
endif

report:
	@$(PYTHON) -c "import json,pathlib; p=pathlib.Path('artefacts/reports/LATEST_EVAL.json'); print(p.read_text(encoding='utf-8')[:5000] if p.exists() else 'MISSING LATEST_EVAL.json')"

queue-demo: up
	$(PYTHON) src/jobqueue/enqueue.py --job p4_eval
	$(PYTHON) src/jobqueue/worker.py --once --timeout 60

worker-once:
	$(PYTHON) src/jobqueue/worker.py --once --timeout 60

# Full suite — no live FT
test:
	$(PYTHON) -m pytest \
		src/ingest/test_p1_contract.py \
		src/ingest/test_p2_ingest.py \
		src/features/test_p3_features.py \
		src/train/test_p4a_train.py \
		src/eval/test_p4b_eval.py \
		src/obs/test_p5a_obs.py \
		src/score/test_fx.py \
		src/jobqueue/test_queue.py \
		src/test_p5b_suite.py \
		-q --tb=line
