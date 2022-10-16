build:
	cd conversion-service && docker compose build

up:
	cd conversion-service && docker compose up

run: build
	cd conversion-service && docker compose up -d

delete:
	cd conversion-service && docker compose down --remove-orphans --volumes 

prune:
	cd conversion-service && docker compose down --remove-orphans --volumes --rmi local

freeze:
	cd conversion-service && python3 -m pip freeze