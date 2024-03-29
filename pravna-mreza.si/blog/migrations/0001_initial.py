# Generated by Django 3.1.10 on 2021-10-08 08:17

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArchivePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.StructBlock([('part_one', wagtail.core.blocks.CharBlock(required=False)), ('part_two', wagtail.core.blocks.CharBlock(required=False))], icon='title'))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField()),
                ('preview_text', wagtail.core.fields.RichTextField(default='')),
                ('body', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.StructBlock([('part_one', wagtail.core.blocks.CharBlock(required=False)), ('part_two', wagtail.core.blocks.CharBlock(required=False)), ('intro_text', wagtail.core.blocks.RichTextBlock(required=False))], icon='title')), ('paragraph', wagtail.core.blocks.RichTextBlock())])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
