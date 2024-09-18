install:
	cd src && pip install -r requirements.txt -t .

test:
	pip install coverage pytest
	coverage run -m pytest

lint:
	pip install flake8
	cd src && flake8 . --count --max-complexity=12 --max-line-length=127 --statistics --exclude pika