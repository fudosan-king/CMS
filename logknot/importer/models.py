from django_mongoengine import Document, EmbeddedDocument, fields  # noqa
import datetime


class LogsImport(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    import_done = fields.DictField(blank=True, default={})
    ignore_buildings = fields.DictField(blank=True, default={})
    import_fail = fields.ListField(blank=True, default=[])
