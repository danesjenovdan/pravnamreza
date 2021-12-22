# Generated by Django 3.1.14 on 2021-12-22 11:55

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_auto_20211222_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footersettings',
            name='footer_links_left',
            field=wagtail.core.fields.StreamField([('page_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(help_text='Če je prazno se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(label='Stran')), ('has_border', wagtail.core.blocks.BooleanBlock(label='Gumb ima obrobo?', required=False))])), ('external_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Ime')), ('url', wagtail.core.blocks.URLBlock(label='Povezava')), ('has_border', wagtail.core.blocks.BooleanBlock(label='Gumb ima obrobo?', required=False))])), ('email_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Ime')), ('email', wagtail.core.blocks.EmailBlock(label='Email povezava'))]))], verbose_name='Povezave v nogi na levi'),
        ),
        migrations.AlterField(
            model_name='footersettings',
            name='footer_links_right',
            field=wagtail.core.fields.StreamField([('page_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(help_text='Če je prazno se uporabi naslov strani.', label='Ime', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(label='Stran')), ('has_border', wagtail.core.blocks.BooleanBlock(label='Gumb ima obrobo?', required=False))])), ('external_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Ime')), ('url', wagtail.core.blocks.URLBlock(label='Povezava')), ('has_border', wagtail.core.blocks.BooleanBlock(label='Gumb ima obrobo?', required=False))])), ('email_link', wagtail.core.blocks.StructBlock([('name', wagtail.core.blocks.CharBlock(label='Ime')), ('email', wagtail.core.blocks.EmailBlock(label='Email povezava'))]))], verbose_name='Povezave v nogi na desni'),
        ),
    ]
