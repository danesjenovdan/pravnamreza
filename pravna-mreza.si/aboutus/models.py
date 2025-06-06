from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from home.models import Publication


class AboutUsPage(Page):
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
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_first"),
        FieldPanel("headline_second"),
        FieldPanel("headline_image"),
        FieldPanel("body"),
    ]

    # seznam medijskih objav
    def get_context(self, request):
        context = super().get_context(request)
        all_publications = Publication.objects.all().order_by("-date")
        paginator = Paginator(all_publications, 10)
        page = request.GET.get("page")
        try:
            publications = paginator.page(page)
        except PageNotAnInteger:
            publications = paginator.page(1)
        except EmptyPage:
            publications = paginator.page(paginator.num_pages)
        context["publications"] = publications
        return context

    class Meta:
        verbose_name = "O nas"
        verbose_name_plural = "O nas"
