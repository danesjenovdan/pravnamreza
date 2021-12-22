# Generated by Django 3.1.14 on 2021-12-17 13:08

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='heading',
            field=models.TextField(blank=True, verbose_name='Naslov'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='intro_text',
            field=wagtail.core.fields.RichTextField(blank=True, null=True, verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('paragraph', wagtail.core.blocks.RichTextBlock())]),
        ),
    ]