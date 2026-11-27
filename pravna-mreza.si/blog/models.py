from django.db import models
from django.http import QueryDict
from django.utils.text import slugify
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from home.pagination import paginate_limit_offset
from home.utils import get_referrer_params


class BlogTag(models.Model):
    name = models.TextField(
        verbose_name="Ime",
    )
    is_fundraiser = models.BooleanField(
        default=False,
        verbose_name="Je zbiranje sredstev",
    )

    @property
    def slug(self):
        return slugify(self.name)

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

    parent_page_types = ["BlogArchivePage", "NewsletterArchivePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["blogpost_archive"] = self.get_parent().url
        return context

    class Meta:
        verbose_name = "Objava"
        verbose_name_plural = "Objave"


class FundraiserPage(BlogPage):
    is_active_fundraiser = models.BooleanField(
        default=True,
        verbose_name="Aktivno zbiranje sredstev",
    )
    fundraiser_slug = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Oznaka za donacije na 'podpri' strani, ki se uporabi za embed donacij",
    )

    content_panels = [
        panel
        for panel in BlogPage.content_panels
        if not isinstance(panel, FieldPanel) or panel.field_name != "tag"
    ] + [
        FieldPanel("is_active_fundraiser"),
        FieldPanel("fundraiser_slug"),
    ]

    parent_page_types = ["FundraiserArchivePage"]

    def get_context(self, request):
        context = super().get_context(request)

        embed_url = f"https://moj.djnd.si/{self.fundraiser_slug}/doniraj"
        campaign = self.title

        if "?" in embed_url:
            embed_url += "&"
        else:
            embed_url += "?"

        referrer_params = get_referrer_params(request)
        default_params_string = f"referrer=pravna-mreza.si&utm_source=pravna-mreza.si&utm_medium=website&utm_campaign={campaign}"
        query_dict = QueryDict(default_params_string, mutable=True)
        for key, value in referrer_params.items():
            if value:
                query_dict[key] = value
        embed_url += query_dict.urlencode()

        context["embed_url"] = embed_url
        return context

    def save(self, *args, **kwargs):
        fundraiser_tag, created = BlogTag.objects.get_or_create(
            is_fundraiser=True,
            defaults={"name": "Zbiranje sredstev"},
        )
        self.tag = fundraiser_tag
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Zbiranje sredstev"
        verbose_name_plural = "Zbiranja sredstev"


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

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "BlogPage"]

    def get_context(self, request):
        context = super().get_context(request)

        tags = BlogTag.objects.all().order_by("name")
        context["tags"] = tags

        selected_tag = None
        slug_to_tag = {tag.slug: tag for tag in tags}
        if tag_slug := request.GET.get("tag", None):
            selected_tag = slug_to_tag.get(tag_slug, None)
        context["selected_tag"] = selected_tag

        all_blogposts = (
            BlogPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        if selected_tag:
            all_blogposts = all_blogposts.filter(tag=selected_tag)
        context["blogposts"] = paginate_limit_offset(all_blogposts, limit=12, offset=0)
        return context

    class Meta:
        verbose_name = "Seznam objav"
        verbose_name_plural = "Seznami objav"


class NewsletterArchivePage(Page):
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

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "BlogPage"]

    def get_context(self, request):
        context = super().get_context(request)
        all_blogposts = (
            BlogPage.objects.child_of(self)
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        context["blogposts"] = paginate_limit_offset(all_blogposts, limit=12, offset=0)
        return context

    class Meta:
        verbose_name = "Seznam novičnikov"
        verbose_name_plural = "Seznami novičnikov"


class FundraiserArchivePage(Page):
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )
    active_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Naslov aktualnih zbiranj",
    )
    archived_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Naslov arhiviranih zbiranj",
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
        FieldPanel("active_title"),
        FieldPanel("archived_title"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.GenericPage", "FundraiserPage"]

    def get_context(self, request):
        context = super().get_context(request)
        active_fundraisers = (
            FundraiserPage.objects.child_of(self)
            .live()
            .filter(is_active_fundraiser=True)
            .order_by("-date", "-first_published_at", "id")
        )
        archived_fundraisers = (
            FundraiserPage.objects.child_of(self)
            .live()
            .filter(is_active_fundraiser=False)
            .order_by("-date", "-first_published_at", "id")
        )
        context["active_fundraisers"] = active_fundraisers
        context["archived_fundraisers"] = archived_fundraisers
        return context

    class Meta:
        verbose_name = "Seznam zbiranja sredstev"
        verbose_name_plural = "Seznami zbiranja sredstev"
