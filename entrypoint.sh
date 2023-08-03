#!/bin/sh
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

python3 manage.py crontab add

#python3 manage.py runserver 0.0.0.0:8000


gunicorn --bind 0.0.0.0:8000 --timeout 900 networkBrahma.wsgi 
