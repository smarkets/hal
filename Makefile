.PHONY: all virtualenv

virtualenv: ./env/requirements.built

./env/requirements.built: requirements.txt
	rm -rf env
	virtualenv --distribute env
	./env/bin/pip install -r requirements.txt
	cp requirements.txt ./env/requirements.built
