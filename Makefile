build:
	cd conversion-service && docker compose build

dev-build:
	cd conversion-service && docker compose -f dev-docker-compose.yaml build

up:
	cd conversion-service && docker compose up

cloud-web-build:
	cd conversion-service && docker compose -f cloud-web-docker-compose.yaml build

cloud-web-run: cloud-web-build
	cd conversion-service && docker compose -f cloud-web-docker-compose.yaml up

cloud-daemon-build:
	cd conversion-service && docker compose -f cloud-daemon-docker-compose.yaml build

cloud-daemon-run: cloud-daemon-build
	cd conversion-service && docker compose -f cloud-daemon-docker-compose.yaml up

run: build
	cd conversion-service && docker compose up -d

dev-up: dev-build
	cd conversion-service && docker compose -f dev-docker-compose.yaml up

dev-prune:
	cd conversion-service && docker compose -f dev-docker-compose.yaml down --remove-orphans --volumes --rmi local

delete:
	cd conversion-service && docker compose down --remove-orphans --volumes 

prune:
	cd conversion-service && docker compose down --remove-orphans --volumes --rmi local

freeze:
	cd conversion-service && python3 -m pip freeze

start-metrics-services:
	docker compose up -d

metrics-prune:
	docker compose down --remove-orphans --volumes --rmi local