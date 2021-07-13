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


### Update locations and railroad

```
cd ~/project/wagtail
. ./env/bin/activate
cd logknot
python3 manage.py locations -p ~/maf4c.txt
python3 manage.py railroad

```

### API

http://cms.localhost:5000/api/locations/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E7%B7%B4%E9%A6%AC%E5%8C%BA/%E4%B8%AD%E6%9D%91%E5%8C%97/ <br>
http://cms.localhost:5000/api/railroad/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E6%88%90%E7%94%B0%E3%82%B9%E3%82%AB%E3%82%A4%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9/


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
