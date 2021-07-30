#!/bin/sh
# Stop uwsgi
# sudo kill -9 [PID]

export LD_LIBRARY_PATH=/usr/local/lib

chmod +r /var/log/uwsgi

cd ~/CMS/logknot
export LANG=ja_JP.UTF-8
exec 2>&1
exec ../env/bin/uwsgi ../etc/production/uwsgi.ini &
