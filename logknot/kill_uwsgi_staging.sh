#!/bin/sh

sudo kill -9 $(ps aux | grep '../env/bin/uwsgi ../etc/staging/uwsgi.ini' | awk '{print $2}')
