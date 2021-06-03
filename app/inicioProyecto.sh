#!/bin/bash

sleep 15

set -x
host="bd"

POSTGRES_PASSWORD='PdL2020'
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "lania" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

python3 -u manage.py makemigrations
python3 -u manage.py migrate
gunicorn --bind :8000 adminServer.wsgi:application --reload
#python3 -u manage.py runserver 0.0.0.0:8000

