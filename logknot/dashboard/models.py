from django_mongoengine import Document, fields, QuerySet
import datetime
from django.conf import settings
from bson import ObjectId


class Buildings(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    building_name = fields.StringField(max_length=255)
    removed = fields.BooleanField(default=False)


class MediaQuerySet(QuerySet):
    def media_by_building(self, building_id):
        return self.filter(building_id=building_id)


class Media(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    file_type = fields.StringField(max_length=10)
    building_id = fields.ObjectIdField()
    meta = {'queryset_class': MediaQuerySet}


def media_path(building_id):
    media = Media.objects.media_by_building(ObjectId(building_id))
    media_path = []
    for m in media:
        media_path.append('{}{}/{}.{}'.format(settings.MEDIA_BUILDINGS, m.building_id, m.id, m.file_type))
    return media_path
