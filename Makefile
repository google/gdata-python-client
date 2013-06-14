PYTHONPATH := src

test:
	 python tests/all_tests_local.py

docs:
	cd docs && sh generate_docs
