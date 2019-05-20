install-deps:
	pip install -r requirements.txt

test:
	export PYTHONPATH=.; \
	python -m unittest tests/test_pepreader.py
	python -m unittest tests/test_pep.py
