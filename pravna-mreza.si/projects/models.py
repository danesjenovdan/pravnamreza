from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

# class ProjectTag(models.Model):
#     name = models.TextField()

#     def __str__(self):
#         return self.name


class ProjectsBlock(blocks.StructBlock):
    project = blocks.PageChooserBlock(page_type="projects.ProjectPage")

    class Meta:
        label = _("Projekt")


class ProjectPage(Page):
    # date = models.DateField()
    preview_text = RichTextField(blank=False, null=False, default="")
    # tag = models.ForeignKey(ProjectTag, on_delete=models.SET_NULL, null=True, blank=True)
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
        # FieldPanel('date'),
        # FieldPanel('tag'),
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
        try:
            projects_archive = ProjectsArchivePage.objects.first().url
        except:
            projects_archive = "/"
        context["projects_archive"] = projects_archive
        return context

    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekti"


class ProjectsArchivePage(Page):
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
    projects = StreamField(
        [
            ("project", ProjectsBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_first"),
        FieldPanel("headline_second"),
        FieldPanel("headline_image"),
        FieldPanel("projects"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "ProjectPage"]

    # def get_context(self, request):
    #     # Update context to include only published posts, ordered by reverse-chron
    #     context = super().get_context(request)
    #     # all_projects = ProjectPage.objects.all().live().order_by("-first_published_at")
    #     all_projects = self.projects
    #     paginator = Paginator(all_projects, 10)
    #     context["projects"] = paginator.get_page(request.GET.get("page"))
    #     return context

    class Meta:
        verbose_name = "Seznam projektov"
        verbose_name_plural = "Seznami projektov"
