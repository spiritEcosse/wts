test_verbose:
	python -m pytest tests/ -vv

test:
	python -m pytest tests/
	# PYTHONPATH=. py.test
