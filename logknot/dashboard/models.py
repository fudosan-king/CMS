from django_mongoengine import Document, fields, QuerySet
import datetime
from django.conf import settings
from bson import ObjectId
from mongoengine.queryset.visitor import Q


class Buildings(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    building_name = fields.StringField(max_length=255)
    removed = fields.BooleanField(default=False)
    create_by = fields.StringField(max_length=255, default='system')
    last_time_remove = fields.DateTimeField(default=datetime.datetime.now)
    remove_by = fields.StringField(max_length=255, default='system')
    last_time_update = fields.DateTimeField(default=datetime.datetime.now)
    update_by = fields.StringField(max_length=255, default='system')
    last_time_rollback = fields.DateTimeField(default=datetime.datetime.now)
    rollback_by = fields.StringField(max_length=255, default='system')

    def query(self, request, removed=False):
        q = Q(removed=removed)
        if request.GET.get('building_name', None):
            q &= Q(building_name=request.GET.get('building_name', None))
        return q


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


class PhotosBuildings():
    def media_path(self, media_id):
        media = Media.objects(id=ObjectId(media_id)).first()
        if not media:
            return '/static/images/no-image.png'
        return '{}{}/{}.{}'.format(settings.MEDIA_BUILDINGS, media.building_id, media.id, media.file_type)
