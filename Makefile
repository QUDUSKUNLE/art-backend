compose:
	cp docker-compose.yml.template docker-compose.yml

start:
	docker-compose build
	docker-compose up

exec:
	docker-compose exec art-backend /bin/bash -it

open:
	open http://0.0.0.0:8000/admin
