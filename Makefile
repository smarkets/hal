.PHONY: all build_virtualenv

run: virtualenv
	PYTHONPATH=. ./env/bin/python main.py

virtualenv: requirements.built

requirements.built: requirements.txt
	rm -rf env
	virtualenv --distribute env
	./env/bin/pip install -r requirements.txt
	cp requirements.txt requirements.built
