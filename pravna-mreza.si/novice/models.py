from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class NovicaTag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class NovicaPage(Page):
    date = models.DateField()
    preview_text = RichTextField(blank=False, null=False, default="")
    tag = models.ForeignKey(NovicaTag, on_delete=models.SET_NULL, null=True, blank=True)
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    intro_text = RichTextField(blank=True, null=True, verbose_name="Opis")
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    meta_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="OG slika",
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("tag"),
        FieldPanel("preview_text", classname="full"),
        FieldPanel("preview_image"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("meta_image"),
    ]

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)
        try:
            homepage = Page.objects.get(slug="home")
            novice_archive = homepage.specific.news_section_archive_link.url
        except:
            novice_archive = "/"
        context["novice_archive"] = novice_archive
        return context

    class Meta:
        verbose_name = "Novica"
        verbose_name_plural = "Novice"


class NovicaArchivePage(Page):
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

    parent_page_types = []

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # Get all novice
        vse_novice = NovicaPage.objects.all().live().order_by("-date")
        # Paginate all novice by 2 per page
        paginator = Paginator(vse_novice, 10)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            novice = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            novice = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            novice = paginator.page(paginator.num_pages)
        context["novice"] = novice
        return context

    class Meta:
        verbose_name = "Seznam novic"
        verbose_name_plural = "Seznami novic"
