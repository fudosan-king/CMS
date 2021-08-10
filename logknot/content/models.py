from django import forms  # noqa
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from rest_framework.fields import Field
from wagtail.api import APIField
from wagtail.admin.edit_handlers import (  # noqa
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from home.streams import blocks
from django.utils.translation import gettext as _  # noqa
from django.db import models
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from django.http import Http404
from bson import ObjectId
from django.urls import reverse
from django.conf import settings
from dashboard.models import Buildings


class CustomTabbedInterface(TabbedInterface):
    def get_form_class(self):
        form_class = super().get_form_class()
        request = self.request

        if request and request.method != 'POST':
            building_id = None
            if not request.get_full_path().endswith('/edit/'):
                building_id = request.GET.get('building_id')
                if not building_id:
                    raise Http404
                try:
                    ObjectId(building_id)
                except:
                    raise Http404
                try:
                    content = ContentDetailPage.objects.filter(building_id=building_id).get()
                except:
                    content = None
                if content:
                    raise Http404

                def initiate_class(**kwargs):
                    if building_id:
                        building = Buildings.objects.filter(id=building_id, removed=False).first()
                        kwargs['initial'] = {
                            'building_id': building.id,
                            'title': building.building_name,
                            'slug': building.building_name,
                            'link': '{}{}'.format(settings.BASE_URL, reverse('buildings_show', args=(building.id,)))
                        }

                    return form_class(**kwargs)

                return initiate_class

        return form_class


class ContentChildPagesSerializer(Field):
    def to_representation(self, child_pages):
        return_posts = []
        for child in child_pages:
            post_dict = {
                'id': child.id,
                'title': child.title,
                'slug': child.slug,
                'url': child.url,
            }
            return_posts.append(post_dict)
        return return_posts


class ContentPage(Page):
    subpage_types = ['content.ContentDetailPage']

    api_fields = [
        APIField('posts', serializer=ContentChildPagesSerializer(source='get_child_pages')),
    ]

    @property
    def get_child_pages(self):
        return self.get_children().public().live()


class ContentDetailPage(Page):
    subpage_types = []
    parent_page_types = ['content.ContentPage']
    building_id = models.CharField(max_length=255, blank=False)
    link = models.URLField(blank=True, null=True)

    content = StreamField(
        [
            ('full_richtext', blocks.RichtextBlock(features=[
                'h1', 'h2', 'h3', 'h4', 'bold', 'italic',
                'ol', 'ul', 'hr', 'link', 'image', 'embed'
                'code', 'superscript', 'subscript', 'strikethrough',
                'blockquote', 'center'])),
        ],
        null=False,
        blank=False,
        verbose_name=_('Content')
    )

    content_panels = Page.content_panels + [
        FieldPanel('building_id'),
        FieldPanel('link'),
        StreamFieldPanel('content'),
    ]

    api_fields = [
        APIField('content'),
    ]

    edit_handler = CustomTabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    def save(self, *args, **kwargs):
        """Create a template fragment key."""
        """Then delete the key."""
        key = make_template_fragment_key(
            'content_building_preview',
            [self.id]
        )
        cache.delete(key)
        return super().save(*args, **kwargs)
