from django_mongoengine import Document, EmbeddedDocument, fields  # noqa
import datetime
from mongoengine.queryset.visitor import Q
from django.core.validators import *  # noqa


class Photos(EmbeddedDocument):
    path = fields.StringField(max_length=255, blank=True)
    category = fields.StringField(max_length=255, blank=True)
    comment = fields.StringField(max_length=255, blank=True)


class Buildings(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    building_name = fields.StringField(max_length=255)
    removed = fields.BooleanField(default=False, blank=True)
    create_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_remove = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    remove_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_update = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    update_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_rollback = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    rollback_by = fields.StringField(max_length=255, default='system', blank=True)
    photos = fields.ListField(
        fields.EmbeddedDocumentField('Photos'),
        blank=True,
        default=[]
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
        self.photos = []
        path = request.POST.getlist('path', [])
        category = request.POST.getlist('category', [])
        comment = request.POST.getlist('comment', [])
        if path:
            for i in range(0, len(path)):
                photos = Photos()
                photos.path = path[i]
                if category and len(category):
                    photos.category = category[i]
                if comment and len(comment):
                    photos.comment = comment[i]
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
