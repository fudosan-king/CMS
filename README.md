### Require

```
sudo yum groupinstall "Development Tools"
Python3 >= 3.9.1
pip3 >= 21.1.2
virtualenv >= 20.4.7 (pip3)
Django >= 3.2.4 (pip3)
uwsgi >= 2.0.19.1 (pip3)
nginx
mongoDB >= 4.0
mySQL >= 5.7
```

### How to install?

```
cd ~/project/wagtail
virtualenv env
. ./env/bin/activate
cd logknot
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser

mkdir ~/project/wagtail/logknot/www/tmp
mkdir ~/project/wagtail/logknot/www/logs
mkdir ~/project/wagtail/logknot/www/import
chmod -R 777  ~/project/wagtail/logknot/www
```


### How to run?

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
screen -c .screenrc.develop
````
http://cms.localhost:5000/


## Access database
User: root
Pass: hgLJ8-8FW9#vD[jM

mysql -u root -p
> CREATE USER 'cms_buildings'@'localhost' IDENTIFIED BY 'sP9m%c7cDUy.ey}{'; <br>
> CREATE DATABASE cms_buildings CHARACTER SET utf8 COLLATE utf8_general_ci; <br>
> GRANT ALL PRIVILEGES ON cms_buildings.* TO cms_buildings@localhost WITH GRANT OPTION; <br>
> FLUSH PRIVILEGES; <br>


### Update locations and railroad

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py locations -p ~/maf4c.txt
python3 manage.py railroad

```


### Wagtail languages:

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot/<sub-page>
django-admin makemessages -l ja
django-admin compilemessages -l ja

```


### Migrations:

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py makemigrations
python3 manage.py migrate

```


### API

<a href="http://cms.localhost:5000/api/locations/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E7%B7%B4%E9%A6%AC%E5%8C%BA/%E4%B8%AD%E6%9D%91%E5%8C%97/">Locations</a><br>
<a href="http://cms.localhost:5000/api/railroad/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E6%88%90%E7%94%B0%E3%82%B9%E3%82%AB%E3%82%A4%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9/">Railroad</a>


### How to run shell

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py shell

```

List all command line
```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py

```

Build static (css, js, images, ...)
```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py collectstatic

```

Test import csv

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py import_csv -d True

```

Update count

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py refresh_count

```



### Document
http://docs.mongoengine.org/ <br>
https://docs.mongoengine.org/guide/querying.html <br>
https://docs.wagtail.io/en/stable/ <br>
https://docs.wagtail.io/en/stable/reference/contrib/forms/customisation.html <br>
https://github.com/spapas/wagtail-multi-upload <br>
https://jossingram.wordpress.com/2015/04/22/a-list-of-wagtails-streamfield-icons/ <br>
https://github.com/CodingForEverybody/learn-wagtail <br>


```
from dashboard.models import *  # Connect to mongoDB
from home.models import *  # Connect to mySQL
```
