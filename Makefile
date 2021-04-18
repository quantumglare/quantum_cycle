setup:
	flake8 --install-hook git && git config --bool flake8.strict true

lint:
	flake8 ./quantumglare

test-ci-lint: lint

test-ci-unit:
	python -m pytest tests/unit

install:
	pip install -r requirements.txt

image:
	docker build --rm -t quantumglare/app ./