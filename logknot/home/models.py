from django.db import models  # noqa
from mongoengine import *  # noqa

from wagtail.core.models import Page


class HomePage(Page):
    pass


class Estates(Document):
    estate_name = StringField(max_length=50)
