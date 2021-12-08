from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2=j#c64aq8xu5@%^0@9k=q=ogo)!)7w5wcla(*i&u_xh2+2(6k'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']  # noqa

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'ja-jp'

BASE_URL = 'http://cms.localhost:5000'

BUILDING_ID = '614931df7150c517fb4ec330'

try:
    from .local import *  # noqa
except ImportError:
    pass
