NAME=rizthme_container

include .env

run:
	poetry run python3 run.py

prune:
	docker system prune -f

rmi: prune
	docker rmi rizthme -f

build: rmi
	docker build -t rizthme .

shell:
	docker run -it rizthme sh

docker-run: stop prune
	docker run -d -e TOKEN=$(TOKEN) --name $(NAME) rizthme

restart: stop
	docker start $(NAME)

stop:
	docker stop $(NAME)