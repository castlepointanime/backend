setup:
	pip install -r requirements.txt

check:  # TODO separate into production build setup
	python3 -m mypy .
	python3 -m flake8 .

run: setup
	uvicorn app:app --reload --workers 2 --host 0.0.0.0 --port 3001

clean:
	find . -type f -name ‘*.pyc’ -delete