#!/bin/bash

python -m pip install --upgrade pip

pip install --upgrade pippip install --force-reinstall -U setuptools
cd django_sms

pip install -r requirements.txt

if [[ $CREATE_SUPERUSER ]]
then
python manage.py createsuperuser --no-input
fi
``` 
