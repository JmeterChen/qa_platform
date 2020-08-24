#!/bin/ash
nohup celery -A qa_platform worker -B -l info  &
nohup python3 manage.py runserver 0.0.0.0:63456 --insecure




