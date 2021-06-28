from django.db import models  # noqa
from mongoengine import *  # noqa


class Estates(Document):
    estate_name = StringField(max_length=50)
