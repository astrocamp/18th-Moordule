.PHONY: i, start migrations migrate startapp precommit


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

# 先加入要提交的文件 - git add .
# 然後使用 commitizen - poetry run cz commit
