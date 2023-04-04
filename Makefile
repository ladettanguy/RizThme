NAME=rizthme_container

-include .env

python-run:
	poetry run python3 run.py

prune:
	docker system prune -f

rmi: prune
	docker rmi rizthme -f

build: rmi
	docker build -t rizthme .

shell:
	docker exec -it $(NAME) sh

docker-run: prune
	docker run -d -e TOKEN=$(TOKEN) --name $(NAME) rizthme

run: docker-run

restart:
	docker start $(NAME)

stop:
	docker stop $(NAME)