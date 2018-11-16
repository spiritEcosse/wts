deploy:
	docker-compose up --build

deploy_hard:
	docker-compose stop && docker-compose rm -f && docker-compose up --build

ipython_web:
	docker-compose exec web ipython

bash_web:
	docker-compose exec web bash

test_verbose:
	docker-compose exec web python -m pytest tests/ -vv

test:
	docker-compose exec web python -m pytest tests/
	# PYTHONPATH=. py.test

init:
	docker-compose exec web flask db init

migrate:
	docker-compose exec web flask db migrate

upgrade: migrate
	docker-compose exec web flask db upgrade
