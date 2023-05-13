#!/bin/bash

pip install --upgrade pippip install --force-reinstall -U setuptools

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations
python manage.py migrate

