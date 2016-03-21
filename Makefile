PYTHON_VERSION = 2.7
DJANGO_VERSION = 1.9

virtualenv:
	test -d .env || virtualenv -p python$(PYTHON_VERSION) .env

develop: virtualenv
	.env/bin/pip install Django==$(DJANGO_VERSION)

test:
	.env/bin/python setup.py test
