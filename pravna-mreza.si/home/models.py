from django.db import models
from novice.models import NovicaPage
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_snippet
class Infopush(models.Model):
    title = models.TextField(null=True, blank=True)
    text = RichTextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('text', classname="full")
    ]

    def __str__(self):
        return self.title


@register_setting
class OgSettings(BaseSetting):
    og_title = models.CharField(max_length=255)
    og_description = models.CharField(max_length=255)
    og_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    panels = [
        FieldPanel('og_title'),
        FieldPanel('og_description'),
        ImageChooserPanel('og_image'),
    ]


class Objava(models.Model):
    title = models.TextField()
    url = models.URLField()
    source = models.TextField()
    date = models.DateField()

    panels = [
        FieldPanel('title'),
        FieldPanel('url', classname="full"),
        FieldPanel('source'),
        FieldPanel('date'),
    ]

    def __str__(self):
        return self.title


class HomePage(Page):
    intro_text = RichTextField(blank=True, null=True)
    description_text = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro_text', classname="full"),
        FieldPanel('description_text', classname="full")
    ]

    parent_page_types = []

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        novice = NovicaPage.objects.all().live().order_by('-first_published_at')[:3]
        pojavljanja = Objava.objects.all().order_by('-date')[:3]
        context['novice'] = novice
        context['pojavljanja'] = pojavljanja
        return context


class GenericPage(Page):
    body = StreamField([
        ('heading', blocks.StructBlock([
            ('part_one', blocks.CharBlock(required=False)),
            ('part_two', blocks.CharBlock(required=False)),
            ('intro_text', blocks.RichTextBlock(required=False)),
        ], icon='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('DonationEmbed', blocks.StaticBlock(admin_text='Donation embed'))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
