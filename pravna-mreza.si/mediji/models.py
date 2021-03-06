from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from home.models import Objava
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class MedijiArchivePage(Page):
    body = StreamField([
        ('heading', blocks.StructBlock([
            ('part_one', blocks.CharBlock(required=False)),
            ('part_two', blocks.CharBlock(required=False)),
        ], icon='title'))
        ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # Get all novice
        vsa_pojavljanja = Objava.objects.all().order_by('-date')
        # Paginate all novice by 2 per page
        paginator = Paginator(vsa_pojavljanja, 10)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            pojavljanja = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            pojavljanja = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            pojavljanja = paginator.page(paginator.num_pages)
        context['pojavljanja'] = pojavljanja
        return context
