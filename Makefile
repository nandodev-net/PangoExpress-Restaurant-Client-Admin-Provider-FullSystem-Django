run:
	python3.5 manage.py runserver

datos:
	python3.5 manage.py makemigrations
	python3.5 manage.py migrate

sudo:
	python3.5 manage.py createsuperuser