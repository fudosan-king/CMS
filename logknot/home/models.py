from django.db import models  # noqa
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.core.fields import StreamField
from streams import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from django import forms


class HomePage(Page):
    description = models.CharField(max_length=255, default='', blank=True)
    keyword = models.CharField(max_length=255, default='', blank=True)

    og_title = models.CharField(max_length=255, default='', blank=True)
    og_url = models.URLField(max_length=255, default='', blank=True)
    og_description = models.CharField(max_length=255, default='', blank=True)
    og_image = models.ForeignKey(
        'home.BuildingImage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichtextBlock()),
            ('simple_richtext', blocks.SimpleRichtextBlock())
        ],
        null=True,
        blank=True,
        default='',
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', widget=forms.Textarea),
        FieldPanel('keyword', widget=forms.Textarea),
        FieldPanel('og_title', widget=forms.Textarea),
        FieldPanel('og_url', ),
        FieldPanel('og_description', widget=forms.Textarea),
        ImageChooserPanel('og_image'),
        StreamFieldPanel('content')
    ]


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
