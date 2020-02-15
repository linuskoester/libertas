#!/usr/bin/env bash

python manage.py collectstatic --no-input
python manage.py makemigrations libertas authentication
python manage.py migrate
python manage.py shell < createsuperuser.py
gunicorn -b 0.0.0.0:8000 core.wsgi
