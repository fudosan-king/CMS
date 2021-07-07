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

try:
    from .local import *  # noqa
except ImportError:
    pass
