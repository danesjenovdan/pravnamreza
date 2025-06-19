from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from home.models import EmailLinkBlock, ExternalLinkBlock, PageLinkBlock
from home.pagination import paginate_limit_offset


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
    # If this is a migrated page, store the old path for reference
    # This is useful for redirects or if we need to reference the old page
    old_migrated_page_path = models.TextField(
        null=True,
        blank=True,
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
            MonitoringPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        context["monitoring_pages"] = paginate_limit_offset(
            all_monitoring_pages, limit=12, offset=0
        )
        return context

    class Meta:
        verbose_name = "Seznam poročil"
        verbose_name_plural = "Seznam poročil"
