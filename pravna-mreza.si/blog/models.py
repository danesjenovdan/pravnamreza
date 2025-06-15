from django.core.paginator import Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class BlogTag(models.Model):
    name = models.TextField(
        verbose_name="Ime",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Oznaka"
        verbose_name_plural = "Oznake"


class BlogAuthor(models.Model):
    name = models.TextField(
        verbose_name="Ime",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Avtor"
        verbose_name_plural = "Avtorji"


class BlogPage(Page):
    date = models.DateField(
        verbose_name="Datum",
    )
    tag = models.ForeignKey(
        BlogTag,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Oznaka",
    )
    preview_text = RichTextField(
        null=False,
        blank=False,
        default="",
        verbose_name="Opis na seznamu",
    )
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika",
    )
    intro_text = RichTextField(
        null=True,
        blank=True,
        verbose_name="Opis pod naslovom",
    )
    related_blog_posts = StreamField(
        [
            ("blog_post", blocks.PageChooserBlock(label="Povezava do blog zapisa")),
        ],
        blank=True,
        null=True,
        verbose_name="Povezani blog zapisi",
    )
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        verbose_name="Besedilo",
    )
    meta_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="OG slika",
    )
    # If this is a migrated page, store the old path for reference
    # This is useful for redirects or if we need to reference the old page
    old_migrated_page_path = models.TextField(
        null=True,
        blank=True,
    )

    @property
    def authors(self):
        authors = [n.author for n in self.blog_author_relationship.all()]
        return authors

    @property
    def authors_list_string(self):
        return ", ".join([str(elem) for elem in self.authors])

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("tag"),
        InlinePanel("blog_author_relationship", label="Avtorji"),
        FieldPanel("preview_text"),
        FieldPanel("preview_image"),
        FieldPanel("intro_text"),
        FieldPanel("body"),
        FieldPanel("related_blog_posts"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("meta_image"),
    ]

    parent_page_types = ["BlogArchivePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["blogpost_archive"] = self.get_parent().url
        return context

    class Meta:
        verbose_name = "Objava"
        verbose_name_plural = "Objave"


class BlogAuthorRelationship(models.Model):
    blog = ParentalKey(
        "BlogPage",
        related_name="blog_author_relationship",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        "BlogAuthor",
        related_name="+",
        on_delete=models.CASCADE,
        verbose_name="Avtor_ica",
    )

    panels = [
        FieldPanel("author"),
    ]


class BlogArchivePage(Page):
    headline_first = models.TextField(
        blank=True,
        verbose_name="Naslovnica prvi del",
    )
    headline_second = models.TextField(
        blank=True,
        verbose_name="Naslovnica drugi del",
    )
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

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "BlogPage"]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        # Get all blogposts
        all_blogposts = BlogPage.objects.all().live().order_by("-first_published_at")
        paginator = Paginator(all_blogposts, 10)
        context["blogposts"] = paginator.get_page(request.GET.get("page"))
        return context

    class Meta:
        verbose_name = "Seznam objav"
        verbose_name_plural = "Seznami objav"
