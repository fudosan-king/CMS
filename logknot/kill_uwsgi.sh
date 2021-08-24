#!/bin/sh

sudo kill -9 $(ps aux | grep '../env/bin/uwsgi ../etc/production/uwsgi.ini' | awk '{print $2}')
