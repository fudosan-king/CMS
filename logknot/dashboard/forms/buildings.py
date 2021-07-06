from django import forms
from django_mongoengine.forms import DocumentForm, EmbeddedDocumentForm
from dashboard.models import Buildings, Photos
from django.utils.translation import gettext as _  # noqa
from django.utils.translation import gettext_lazy as __  # noqa


class PhotosForm(EmbeddedDocumentForm):
    class Meta:
        document = Photos
        fields = '__all__'
        embedded_field = 'photos'


class BuildingsForm(DocumentForm):
    building_name = forms.CharField(
        label=__('Building Name'),
        max_length=254,
        widget=forms.TextInput()
    )

    class Meta:
        document = Buildings
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
