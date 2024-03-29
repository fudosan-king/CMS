# Generated by Django 3.2.5 on 2021-08-06 01:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import home.streams.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210727_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='article_modified_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Article modified time'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='article_publisher',
            field=models.URLField(blank=True, default='', max_length=255, verbose_name='Article publisher'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='fb_app_id',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Facebook ID'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_locale',
            field=models.CharField(blank=True, default='ja_JP', max_length=10, verbose_name='OG Locale'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_site_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='OG Sitename'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='og_type',
            field=models.CharField(blank=True, default='article', max_length=20, verbose_name='OG Type'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='robots',
            field=models.CharField(blank=True, default='noindex, nofollow', max_length=255, verbose_name='Robots'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='twitter_card',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Twitter card'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='twitter_creater',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Twitter creater'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='twitter_site',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Twitter site'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Add additional text', required=True))])), ('full_richtext', home.streams.blocks.RichtextBlock()), ('simple_richtext', home.streams.blocks.SimpleRichtextBlock())], blank=True, default='', null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='description',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='keyword',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Keyword'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='og_description',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='OG Description'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='og_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.buildingimage', verbose_name='OG image'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='og_title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='OG Title'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='og_url',
            field=models.URLField(blank=True, default='', max_length=255, verbose_name='OG URL'),
        ),
    ]
