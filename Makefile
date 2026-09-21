PYTHON ?= python3

.PHONY: install lint test coverage run dashboard docker-up docker-down

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install pytest pytest-cov flake8

lint:
	$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

test:
	$(PYTHON) -m pytest -q

coverage:
	$(PYTHON) -m pytest --cov=sie --cov=stock_intelligence_engine --cov-report=term-missing --cov-report=xml

run:
	$(PYTHON) stock_intelligence_engine.py

dashboard:
	streamlit run app.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
