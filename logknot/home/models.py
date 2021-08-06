from django.db import models  # noqa
from wagtail.core.models import Page
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.core.fields import StreamField
from home.streams import blocks
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from django import forms
from django.utils.translation import gettext as _  # noqa
from dashboard.models import Buildings
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render
from django.utils import timezone


class HomePage(RoutablePageMixin, Page):
    description = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Description'))
    keyword = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Keyword'))
    robots = models.CharField(max_length=255, default='noindex, nofollow', blank=True, verbose_name=_('Robots'))

    og_title = models.CharField(max_length=255, default='', blank=True, verbose_name=_('OG Title'))
    og_description = models.CharField(max_length=255, default='', blank=True, verbose_name=_('OG Description'))
    og_url = models.URLField(max_length=255, default='', blank=True, verbose_name=_('OG URL'))
    og_image = models.ForeignKey(
        'home.BuildingImage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_('OG image')
    )
    og_locale = models.CharField(max_length=10, default='ja_JP', blank=True, verbose_name=_('OG Locale'))
    og_type = models.CharField(max_length=20, default='article', blank=True, verbose_name=_('OG Type'))
    og_site_name = models.CharField(max_length=255, default='', blank=True, verbose_name=_('OG Sitename'))
    fb_app_id = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Facebook ID'))
    article_publisher = models.URLField(max_length=255, default='', blank=True, verbose_name=_('Article publisher'))
    article_modified_time = models.DateTimeField(
        auto_now_add=False, default=timezone.now, verbose_name=_('Article modified time'))
    twitter_card = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Twitter card'))
    twitter_creater = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Twitter creater'))
    twitter_site = models.CharField(max_length=255, default='', blank=True, verbose_name=_('Twitter site'))

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichtextBlock()),
            ('simple_richtext', blocks.SimpleRichtextBlock())
        ],
        null=True,
        blank=True,
        default='',
        verbose_name=_('Content')
    )

    content_panels = Page.content_panels + [
        FieldPanel('description', widget=forms.Textarea),
        FieldPanel('keyword', widget=forms.Textarea),
        FieldPanel('og_title', widget=forms.Textarea),
        FieldPanel('og_url', ),
        FieldPanel('og_description', widget=forms.Textarea),
        ImageChooserPanel('og_image'),
        FieldPanel('og_locale', widget=forms.TextInput),
        FieldPanel('og_type', widget=forms.TextInput),
        FieldPanel('og_site_name', widget=forms.Textarea),
        FieldPanel('fb_app_id', widget=forms.TextInput),
        FieldPanel('article_publisher', ),
        FieldPanel('article_modified_time', widget=forms.DateTimeInput),
        FieldPanel('twitter_card', widget=forms.TextInput),
        FieldPanel('twitter_creater', widget=forms.TextInput),
        FieldPanel('twitter_site', widget=forms.TextInput),
        StreamFieldPanel('content')
    ]

    def get_buildings_recommend(self, *args, **kwargs):
        return Buildings.objects().filter(removed=False, recommend=True).all()

    def get_buildings_new(self, *args, **kwargs):
        return Buildings.objects().filter(removed=False).order_by('-created_at')[:16]

    @route(r'^company/', name='company')
    def company_page(self, request):
        context = self.get_context(request)
        return render(request, 'www/company.html', context)


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
