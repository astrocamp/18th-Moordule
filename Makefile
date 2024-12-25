
.PHONY: shell start migrations migrate startapp precommit commit users meetups records


shell:
	poetry run python manage.py shell
	
start:
	poetry run python manage.py runserver

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

startapp:
	poetry run python manage.py startapp ${name}

precommit:
	poetry run pre-commit run --all-files

commit:
	poetry run cz commit

server:
	python manage.py runserver

migtion:
	python manage.py makemigrations

mig:
	python manage.py migrate

users:
	python manage.py generate_fake_users --count 20

meetups:
	python manage.py generate_fake_meetups --count 30

records:
	python manage.py generate_fake_records --count 10 --force