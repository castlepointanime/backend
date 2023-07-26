setup:
	pip install -r requirements.txt

check:  # TODO separate into production build setup
	python3 -m mypy .
	python3 -m flake8 .

run: setup check
	gunicorn app:app -w 2 --reload --threads 2 -b 0.0.0.0:3001

clean:
	find . -type f -name ‘*.pyc’ -delete