#!/usr/bin/env bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(export LC_ALL=C) &
(gunicorn display_stock.wsgi --user www-data --bind 0.0.0.0:8010 --timeout 600) &
nginx -g "daemon off;"
