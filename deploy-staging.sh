#!/bin/sh
rsync --delete -e  'ssh -i deployment/fdk-production.pem' -rlpcgz -v --exclude-from=excludes ./ ec2-user@3.112.126.123:/var/www/wagtail/
ssh -i deployment/fdk-production.pem ec2-user@3.112.126.123 -t 'cd /var/www/wagtail/logknot && ./kill_uwsgi_staging.sh'
ssh -i deployment/fdk-production.pem -t ec2-user@3.112.126.123 "sh -c 'cd /var/www/wagtail/logknot; nohup ./uwsgi_staging.sh > /dev/null 2>&1'"
