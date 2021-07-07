### Require

```
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
sudo mkdir /var/log/uwsgi
sudo mkdir /var/log/nginx
sudo chmod 777 /var/log/uwsgi
sudo chmod 777 /var/log/nginx
cd ~/project/wagtail
virtualenv env
. ./env/bin/activate
cd logknot
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
```



### How to run?

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
screen -c .screenrc.develop
````
http://cms.localhost:5000/


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



### Document
http://docs.mongoengine.org/ <br>
https://docs.wagtail.io/en/stable/ <br>
https://docs.wagtail.io/en/stable/reference/contrib/forms/customisation.html <br>
https://github.com/spapas/wagtail-multi-upload <br>
