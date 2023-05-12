#!/bin/bash

python -m pip install --upgrade pip

pip install --upgrade pippip install --force-reinstall -U setuptools
cd django_sms

pip install -r requirements.txt

if [[ $CREATE_SUPERUSER ]]
then
python manage.py createsuperuser --noinput --username $SUPERUSER_NAME --email $SUPERUSER_EMAIL
fi
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
 
