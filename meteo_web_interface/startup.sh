#!/bin/bash

celery -A meteo_web_interface worker -B &
redis-server &
gunicorn meteo_web_interface.wsgi -b :8080
