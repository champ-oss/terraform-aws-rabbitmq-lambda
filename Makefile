install:
	cd src && pip install -r requirements.txt

freeze:
	cd src && pip freeze > requirements.txt

test:
	pip install coverage pytest
	coverage run -m pytest

lint:
	pip install flake8
	cd src && flake8 . --count --max-complexity=12 --max-line-length=127 --statistics --exclude venv

docker:
	docker build -t terraform-aws-rabbitmq-lambda .
	docker run -it terraform-aws-rabbitmq-lambda

coverage:
	coverage run -m pytest
	coverage html --omit="test_*.py"
	coverage xml --omit="test_*.py"
	open htmlcov/index.html || true

check-coverage:
	coverage run -m pytest
	coverage xml --omit="test_*.py"
	coverage report --fail-under=80