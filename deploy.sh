#!/bin/sh
# rsync --delete -e  'ssh -i deployment/fdk-production.pem' -rlpcgz -v --exclude-from=excludes ./ ec2-user@54.238.184.234:/var/www/CMS/
ssh database@fudosan-king.xyz -t 'cd ~/CMS && git pull --rebase'
ssh database@fudosan-king.xyz -t 'cd ~/CMS/logknot && ./kill_uwsgi.sh'
ssh -t database@fudosan-king.xyz "sh -c 'cd ~/CMS/logknot; nohup ./uwsgi.sh > /dev/null 2>&1'"
