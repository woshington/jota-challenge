migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate


create_superuser:
	poetry run python manage.py createsuperuser