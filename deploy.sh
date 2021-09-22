#!/bin/sh
rsync --delete -e  'ssh -i deployment/fdk-production.pem' -rlpcgz -v --exclude-from=excludes ./ ec2-user@13.115.246.53:/var/www/wagtail/
ssh -i deployment/fdk-production.pem ec2-user@13.115.246.53 -t 'cd /var/www/wagtail/logknot && ./kill_uwsgi.sh'
ssh -i deployment/fdk-production.pem -t ec2-user@13.115.246.53 "sh -c 'cd /var/www/wagtail/logknot; nohup ./uwsgi.sh > /dev/null 2>&1'"
