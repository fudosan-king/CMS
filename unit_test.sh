#!/bin/sh

flake8 --statistics --count --exclude='./env/,./etc/,*/migrations/,*/migrations_/' --max-line-length=119 . --ignore=E722,W504
