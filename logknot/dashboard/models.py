from django_mongoengine import Document, fields
import datetime
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
