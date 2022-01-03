# Generated by Django 3.1.14 on 2021-12-23 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('novice', '0007_auto_20211220_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='novicapage',
            name='meta_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='OG slika'),
        ),
    ]