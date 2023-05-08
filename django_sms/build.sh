#!/bin/bash

pip install --upgrade pippip install --force-reinstall -U setuptools

pip install -r requirements.txt

if [[ $CREATE_SUPERUSER ]]
then 
python django_sms/manage.py createsuperuser --no-input
fi
