# Generated by Django 3.1.14 on 2021-12-26 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('home', '0037_auto_20211222_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletterpage',
            name='headline_first',
            field=models.TextField(blank=True, verbose_name='Naslovnica prvi del'),
        ),
        migrations.AddField(
            model_name='newsletterpage',
            name='headline_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Slika na naslovnici'),
        ),
        migrations.AddField(
            model_name='newsletterpage',
            name='headline_second',
            field=models.TextField(blank=True, verbose_name='Naslovnica drugi del'),
        ),
    ]