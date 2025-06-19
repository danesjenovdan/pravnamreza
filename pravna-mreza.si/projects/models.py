from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class ProjectsBlock(blocks.StructBlock):
    project = blocks.PageChooserBlock(page_type="projects.ProjectPage")

    class Meta:
        label = _("Projekt")


class ProjectPage(Page):
    preview_text = RichTextField(blank=False, null=False, default="")
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
        FieldPanel("preview_text", classname="full"),
        FieldPanel("preview_image"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("meta_image"),
    ]

    parent_page_types = ["ProjectsArchivePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["projects_archive"] = self.get_parent().url
        return context

    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekti"


class ProjectsArchivePage(Page):
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )
    projects_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Naslov aktualnih projektov",
    )
    projects = StreamField(
        [
            ("project", ProjectsBlock()),
        ],
        null=True,
        blank=True,
        verbose_name="Aktualni projekti",
    )
    archived_projects_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Naslov arhiviranih projektov",
    )
    archived_projects = StreamField(
        [
            ("project", ProjectsBlock()),
        ],
        null=True,
        blank=True,
        verbose_name="Arhivirani projekti",
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
        FieldPanel("projects_title"),
        FieldPanel("projects"),
        FieldPanel("archived_projects_title"),
        FieldPanel("archived_projects"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "ProjectPage"]

    class Meta:
        verbose_name = "Seznam projektov"
        verbose_name_plural = "Seznami projektov"
