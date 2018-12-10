deploy:
	docker-compose up

deploy_detach:
	docker-compose up -d

deploy_build:
	docker-compose up --build

deploy_hard:
	docker-compose stop && docker-compose rm -f && docker-compose up -d --build

ipython:
	docker-compose exec web ipython

freeze:
	docker-compose exec web pip freeze > requirements.txt

bash:
	docker-compose exec web bash

cov:
	docker-compose exec web ./test_cov.sh

test_all:
	docker-compose exec web ./test.sh
	# PYTHONPATH=. py.test
	# verbose - -vv

init:
	docker-compose exec web flask db init --multidb

migrate:
	docker-compose exec web flask db migrate

upgrade: migrate
	docker-compose exec web flask db upgrade

downgrade:
	docker-compose exec web flask db downgrade
