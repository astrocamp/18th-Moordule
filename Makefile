shell:
	python manage.py shell
	
start:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

startapp: 
	python manage.py startapp ${name}

precommit:
	pre-commit run --all-files

commit: 
	cz commit

# 先加入要提交的文件 - git add .
# 然後使用 commitizen - poetry run cz commit
