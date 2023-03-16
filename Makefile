NAME=rizthme_container

run:
	poetry run python3 run.py

echo:
	echo "Je suis echo"

prune:
	docker system prune -f

rmi: prune
	docker rmi rizthme -f

build: rmi
	docker build -t rizthme .

shell:
	docker run -it rizthme sh

docker-run: prune
	docker run -d -e TOKEN=$(TOKEN) --name $(NAME) rizthme

stop:
	docker stop $NAME