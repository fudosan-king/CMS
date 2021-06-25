### Require

```
Python3 >= 3.9.1
pip3 >= 21.1.2
virtualenv >= 20.4.7 (pip3)
Django >= 3.2.4 (pip3)
```


### How to install?

```
cd ~/project/wagtail
virtualenv env
. ./env/bin/activate
pip3 install wagtail
wagtail start logknot
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
python3 manage.py runserver
````
