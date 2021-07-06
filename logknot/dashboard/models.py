from django_mongoengine import Document, EmbeddedDocument, fields  # noqa
import datetime
from mongoengine.queryset.visitor import Q
from django.core.validators import *  # noqa


class Photos(EmbeddedDocument):
    url = fields.StringField(max_length=255)
    category = fields.StringField(max_length=255)
    comment = fields.StringField(max_length=255)


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
    photos = fields.ListField(
        fields.EmbeddedDocumentField('Photos'),
        blank=True,
        default=[],
    )

    @staticmethod
    def building_name_validation(building_name):
        if not building_name:
            raise ValidationError('Not have building name')

    def clean(self):
        self.building_name_validation(self.building_name)

    def query(self, request, removed=False):
        q = Q(removed=removed)
        if request.GET.get('building_name', None):
            q &= Q(building_name=request.GET.get('building_name', None))
        return q

    def update(self, request):
        if request.POST.get('building_name', None):
            self.building_name = request.POST.get('building_name', None)
        self.last_time_update = datetime.datetime.now
        self.update_by = str(request.user)
        photos = Photos()
        photos.url = 'aaaa'
        photos.category = 'bbbb'
        photos.comment = 'cccc'
        self.photos.append(photos)
        return self

    def remove(self, request):
        self.removed = True
        self.last_time_remove = datetime.datetime.now
        self.remove_by = str(request.user)
        return self

    def add(self, request):
        self.create_by = str(request.user)
        return self
