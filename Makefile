
.PHONY: run
run:
	pipenv run hug -nf server.py

.PHONY: test
test:
	pipenv run pytest
