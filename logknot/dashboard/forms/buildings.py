from django import forms
from django_mongoengine.forms import DocumentForm
from dashboard.models import Buildings
from django.utils.translation import gettext as _  # noqa
from django.utils.translation import gettext_lazy as __  # noqa


class BuildingsForm(DocumentForm):
    building_name = forms.CharField(
        label=__("Building Name"),
        max_length=254,
        widget=forms.TextInput()
    )

    class Meta:
        document = Buildings
        fields = "__all__"
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
