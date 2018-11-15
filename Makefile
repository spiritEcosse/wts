deploy:
	docker-compose up --build

deploy_hard:
	docker-compose stop && docker-compose rm -f && docker-compose up --build

ipython_web:
	docker-compose exec web ipython

bash_web:
	docker-compose exec web bash
