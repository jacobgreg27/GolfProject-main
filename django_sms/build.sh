#!/bin/bash

pip install --upgrade pippip install --force-reinstall -U setuptools

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

if [[ $CREATE_SUPERUSER ]]
then 
python manage.py createsuperuser --no-input
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='$SUPERUSER_EMAIL').update(password='$SUPERUSER_PASSWORD')"
fi
password=$password
python manage.py runserver
