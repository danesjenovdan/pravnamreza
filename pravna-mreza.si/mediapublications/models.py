from django.core.paginator import Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from home.models import Publication


class MediaPublicationsPage(Page):
    headline_first = models.TextField(verbose_name="Naslovnica prvi del", blank=True)
    headline_second = models.TextField(verbose_name="Naslovnica drugi del", blank=True)
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_first"),
        FieldPanel("headline_second"),
        FieldPanel("headline_image"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        all_publications = Publication.objects.all().order_by("-date")
        paginator = Paginator(all_publications, 10)
        context["publications"] = paginator.get_page(request.GET.get("page"))
        return context

    class Meta:
        verbose_name = "Objave medijev"
        verbose_name_plural = "Objave medijev"
