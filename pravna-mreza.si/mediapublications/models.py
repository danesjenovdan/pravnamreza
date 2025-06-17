from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from home.models import Publication


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
        publications = all_publications[:12]
        context["publications"] = publications
        context["publications_shown"] = len(publications)
        context["publications_total"] = all_publications.count()
        return context

    class Meta:
        verbose_name = "Objave medijev"
        verbose_name_plural = "Objave medijev"
