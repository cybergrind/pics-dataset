VENV ?= venv
PYTHON_BIN ?= python3.11
PYTHON ?= $(VENV)/bin/python
PYTHONPATH = $(VENV)/lib/$(PYTHON_BIN)/site-packages:backend
PORT ?= 8009
PHONY += build-front


run: venv frontend/pics-dataset/build .logs
	$(VENV)/bin/uvicorn --factory pics_dataset.app:get_app \
		--reload --reload-dir backend/pics_dataset \
		--port $(PORT) --host ::0

.logs:
	mkdir .logs

venv: backend/requirements.txt
	$(PYTHON_BIN) -m venv $(VENV)
	$(VENV)/bin/pip install -r backend/requirements.txt
	touch venv


backend/requirements.txt: backend/requirements.in
	pip-compile --resolver=backtracking --output-file backend/requirements.txt \
		backend/requirements.in


frontend/pics-dataset/build: frontend/pics-dataset/node_modules
	cd frontend/pics-dataset && pnpm run check && pnpm run build


frontend/pics-dataset/node_modules: $(wildcard frontend/pics-dataset/pnpm-lock.yaml)
	cd frontend/pics-dataset && npm install pnpm && pnpm install


build-front:
	cd frontend/pics-dataset && pnpm run check && pnpm run build

dev:
	cd frontend/pics-dataset && pnpm run dev


