test_it_verbose:
	python -m pytest tests/ -vv

test_it:
	python -m pytest tests/
	# PYTHONPATH=. py.test
