#!/bin/sh

flake8 --statistics --count --exclude='./env/,./etc/,./logknot/home/migrations/,./logknot/blog/migrations' --max-line-length=119 . --ignore=E722
