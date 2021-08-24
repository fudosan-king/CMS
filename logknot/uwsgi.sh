#!/bin/sh

cd ~/CMS/logknot
exec ../env/bin/uwsgi ../etc/production/uwsgi.ini &
