from django.core.paginator import Paginator
from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from home.models import EmailLinkBlock, ExternalLinkBlock, PageLinkBlock


class MonitoringPage(Page):
    date = models.DateField()
    preview_text = RichTextField(blank=False, null=False, default="")
    intro_text = RichTextField(blank=True, null=True, verbose_name="Opis")
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("preview_text"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
    ]

    parent_page_types = ["MonitoringArchivePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["monitoring_archive"] = self.get_parent().url
        return context

    class Meta:
        verbose_name = "Poročilo"
        verbose_name_plural = "Poročilo"


class MonitoringArchivePage(Page):
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )
    intro_text = RichTextField(blank=True, null=True, verbose_name="Opis")
    link = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
            ("email_link", EmailLinkBlock()),
        ],
        null=True,
        blank=True,
        verbose_name="Povezava v opisu",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
        FieldPanel("intro_text"),
        FieldPanel("link"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "MonitoringPage"]

    def get_context(self, request):
        context = super().get_context(request)
        all_monitoring_pages = (
            MonitoringPage.objects.all()
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        monitoring_pages = all_monitoring_pages[:12]
        context["monitoring_pages"] = monitoring_pages
        context["monitoring_pages_shown"] = len(monitoring_pages)
        context["monitoring_pages_total"] = all_monitoring_pages.count()
        return context

    class Meta:
        verbose_name = "Seznam poročil"
        verbose_name_plural = "Seznam poročil"
