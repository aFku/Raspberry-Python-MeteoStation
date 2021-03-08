#!/bin/bash

source $HOME/.profile

export PYTHONPATH="$APP_PATH/meteo_web_interface/:$PYTHONPATH"

export GUNICORN="/home/${user}/.local/bin/gunicorn"

export CELERY="/usr/local/bin/celery"

redis-server &

$CELERY -A meteo_web_interface worker -B -l ERROR &

$GUNICORN meteo_web_interface.wsgi -b :8080
