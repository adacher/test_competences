include docker.ini

all: build start
	@sleep 2
	docker ps


build: build-flask-premier build-flask-random build-nginx 

start:
	@echo "###############################"
	@echo "# START DEV CONTAINER"
	@echo "###############################"
	DEBUG= docker-compose up -d

build-flask-premier:
	@echo "################################################################"
	@echo "# BUILD FLASK PREMIER - $(DOCKER_PREMIER_IMG)"
	@echo "################################################################"
	docker-compose build flask-premier

build-flask-random:
	@echo "################################################################"
	@echo "# BUILD FLASK RANDOM - $(DOCKER_RANDOM_IMG)"
	@echo "################################################################"
	docker-compose build flask-random

build-nginx:
	@echo "################################################################"
	@echo "# BUILD NGINX REVERSE PROXY - $(DOCKER_NGINX_IMG)"
	@echo "################################################################"
	docker-compose build nginx

destroy:
	@echo "###############################"
	@echo "# DESTROY CONTAINER"
	@echo "###############################"
	make down

destroy-nginx:
	docker stop $(DOCKER_NGINX_IMG)
	docker rm $(DOCKER_NGINX_IMG)

down:
	docker-compose down -v

rebuild:
	@echo "###############################"
	@echo "# REBUILD CONTAINER"
	@echo "###############################"
	make down
	make

restart:
	@echo "###############################"
	@echo "# RESTART CONTAINER"
	@echo "###############################"
	make stop
	make start

restart-nginx:
	docker stop nginx
	docker rm nginx
	make start

start:
	@echo "###############################"
	@echo "# START DEV CONTAINER"
	@echo "###############################"
	DEBUG= docker-compose up -d


start-debug:
	@echo "###############################"
	@echo "# START DEV CONTAINER"
	@echo "###############################"
	DEBUG=true docker-compose up -d

stop:
	@echo "###############################"
	@echo "# STOP CONTAINER"
	@echo "###############################"
	docker-compose stop


config:
	docker-compose config