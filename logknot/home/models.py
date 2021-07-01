from django.db import models  # noqa
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class HomePage(Page):
    pass


class BuildingImage(AbstractImage):
    building_id = models.CharField(max_length=255, blank=True)
    admin_form_fields = Image.admin_form_fields + (
        'building_id',
    )


class BuildingRendition(AbstractRendition):
    image = models.ForeignKey(BuildingImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
