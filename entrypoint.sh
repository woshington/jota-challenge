#!/bin/sh
set -e

poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:8000
