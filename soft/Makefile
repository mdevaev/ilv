all:
	cat Makefile

tox:
	tox -q -c linters/tox.ini

clean:
	find pixtube -name __pycache__ | xargs rm -rf

clean-all: clean
	rm -rf linters/.{tox,mypy_cache}
