deploy:
	docker-compose up

deploy_hard:
	docker-compose stop && docker-compose rm -f && docker-compose up --build

ipython:
	docker-compose exec web ipython

bash:
	docker-compose exec web bash

test:
	docker-compose exec web ./test.sh
	# PYTHONPATH=. py.test
	# verbose - -vv

init:
	docker-compose exec web flask db init --multidb

migrate:
	docker-compose exec web flask db migrate

upgrade: migrate
	docker-compose exec web flask db upgrade
