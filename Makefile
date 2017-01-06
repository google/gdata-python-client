PYTHONPATH := src

test:
	 python tests/all_tests_local.py

docs:
	cd pydocs && sh generate_docs
