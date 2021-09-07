#!/bin/sh

cd /var/www/wagtail/logknot
exec ../env/bin/uwsgi ../etc/staging/uwsgi.ini &
