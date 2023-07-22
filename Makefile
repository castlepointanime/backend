setup:
	pip install -r requirements.txt

run: setup
	python3 -m mypy .
	gunicorn app:app -w 2 --reload --threads 2 -b 0.0.0.0:3001 --threads 1 -b 0.0.0.0:5000

clean:
	find . -type f -name ‘*.pyc’ -delete