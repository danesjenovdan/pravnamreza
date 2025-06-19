from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from home.models import Publication
from home.pagination import paginate_limit_offset


class MediaPublicationsPage(Page):
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        all_publications = Publication.objects.all().order_by("-date", "id")
        context["publications"] = paginate_limit_offset(
            all_publications, limit=12, offset=0
        )
        return context

    class Meta:
        verbose_name = "Objave medijev"
        verbose_name_plural = "Objave medijev"
