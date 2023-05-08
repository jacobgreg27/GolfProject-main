#!/bin/bash

pip install --upgrade pippip install --force-reinstall -U setuptools

pip install -r requirements.txt

if [[$CREATE_SUPERUSER == "true"]]; then
    python manage.py createsuperuser --noinput
fi