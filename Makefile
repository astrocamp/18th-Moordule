.PHONY: start migrations migrate startapp precommit

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


# 雷雷的python指令

intoshell:
	python manage.py shell
	
server:
	python manage.py runserver

migration:
	python manage.py makemigrations

mi:
	python manage.py migrate

startapps: 
	python manage.py startapp ${name}

precommits:
	pre-commit run --all-files

commits: 
	cz commit

