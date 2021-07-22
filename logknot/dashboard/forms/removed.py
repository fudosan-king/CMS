from django.utils.translation import gettext as _  # noqa
from django.utils.translation import gettext_lazy as __  # noqa
from .buildings import BuildingsForm
from django import forms


class RemovedBuildingsForm(BuildingsForm):
    remove_by = forms.CharField(
        label=__('によって削除されました'),
        widget=forms.TextInput()
    )
    last_time_remove = forms.DateField(
        label=__('前回削除'),
        widget=forms.DateInput()
    )
