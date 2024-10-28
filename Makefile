up:
	docker compose -f ./docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

create:
	alembic revision --autogenerate -m "test"

upgrade:
	 alembic upgrade heads