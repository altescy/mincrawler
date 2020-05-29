PWD=$(shell pwd)
PYTHON=poetry run python
MYPY=poetry run mypy
PYLINT=poetry run pylint
PYLINTRC=.pylintrc
MYPYINI=mypy.ini
PYTEST=poetry run pytest
MODULE=mincrawler
DOCKER=docker
DOCKERFILE=$(PWD)/docker/Dockerfile.dev
DOCKER_IMAGE=mincrawler-dev
DOCKER_CONTAINER=mincrawler-dev-container


lint:
	$(PYLINT) --rcfile=$(PYLINTRC) $(MODULE)

mypy:
	$(MYPY) --config-file $(MYPYINI) $(MODULE)

test:
	PYTHONPATH=$(PWD) $(PYTEST)

clean: clean-pyc clean-build

clean-pyc:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf $(MODULE).egg-info/
	rm -rf pip-wheel-metadata/

docker: docker-build docker-run

docker-build:
	$(DOCKER) build -f $(DOCKERFILE) -t $(DOCKER_IMAGE) $(PWD)

docker-run:
	$(DOCKER) run -it -v $(PWD):/work --name $(DOCKER_CONTAINER) $(DOCKER_IMAGE)

docker-attach:
	$(DOCKER) attach $(DOCKER_CONTAINER)

docker-rm:
	$(DOCKER) rm $(DOCKER_CONTAINER)
