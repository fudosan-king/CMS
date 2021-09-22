from .base import *  # noqa

DEBUG = False

# mySQL setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'cms_buildings',
        'USER': 'cms_buildings',
        'PASSWORD': 'sP9m%c7cDUy.ey}{',
        'TEST': {
            'NAME': 'cms_buildings_test',
        },
    },
    'cms_buildings': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# MongoDB settings
MONGODB_DATABASES = {
    'default': {
        'name': 'cms_buildings',
        'host': 'localhost',
        'tz_aware': True
    }
}

LANGUAGE_CODE = 'ja-jp'

SECRET_KEY = 'django-insecure-2=j#c64aq8xu5@%^0@9k=q=ogo)!)7w5wcla(*i&u_xh2+2(6k'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'msdb.order-renove.jp']  # noqa

BASE_URL = 'https://msdb.order-renove.jp'

try:
    from .local import *  # noqa
except ImportError:
    pass
