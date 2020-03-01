#!/usr/bin/env bash

python manage.py makemigrations libertas authentication viewer
python manage.py migrate
python manage.py shell < createsuperuser.py
python manage.py runserver 0.0.0.0:80
