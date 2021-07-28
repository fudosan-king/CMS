from .base import *  # noqa

DEBUG = False

# mySQL setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'cms_buildings',
        'USER': 'root',
        'PASSWORD': '',
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

SECRET_KEY = 'django-insecure-2=j#c64aq8xu5@%^0@9k=q=ogo)!)7w5wcla(*i&u_xh2+2(6k'

LANGUAGE_CODE = 'ja-jp'

try:
    from .local import *  # noqa
except ImportError:
    pass
