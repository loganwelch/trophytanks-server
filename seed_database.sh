#!/bin/bash

rm db.sqlite3
rm -rf ./tanksapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations tanksapi
python3 manage.py migrate tanksapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata profiles
python3 manage.py loaddata tags
python3 manage.py loaddata tanks