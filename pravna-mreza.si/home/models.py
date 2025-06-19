from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from blog.models import BlogPage


class ExternalLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(label=_("Ime"))
    url = blocks.URLBlock(label=_("Povezava"))
    has_border = blocks.BooleanBlock(label="Gumb ima obrobo?", required=False)

    class Meta:
        label = _("Zunanja povezava")
        icon = "link"


class PageLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(
        required=False,
        label=_("Ime"),
        help_text=_("Če je prazno se uporabi naslov strani."),
    )
    page = blocks.PageChooserBlock(label=_("Stran"))
    has_border = blocks.BooleanBlock(label="Gumb ima obrobo?", required=False)

    class Meta:
        label = _("Povezava do strani")
        icon = "link"


class EmailLinkBlock(blocks.StructBlock):
    name = blocks.CharBlock(label=_("Ime"))
    email = blocks.EmailBlock(label=_("Email povezava"))

    class Meta:
        label = _("Email povezava")
        icon = "link"


class Infopush(models.Model):
    title = models.TextField(verbose_name="Naslov")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika (neobvezno)",
    )
    text = RichTextField(verbose_name="Opis")
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Povezava do strani (neobvezno)",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        FieldPanel("text", classname="full"),
        PageChooserPanel("page"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Infopush"
        verbose_name_plural = "Infopushi"


@register_setting
class OgSettings(BaseGenericSetting):
    og_title = models.CharField(max_length=255)
    og_description = models.CharField(max_length=255)
    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("og_title"),
        FieldPanel("og_description"),
        FieldPanel("og_image"),
    ]


@register_setting()
class NavigationSettings(BaseGenericSetting):
    navigation_links = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
        ],
        verbose_name=_("Povezave v glavi"),
        use_json_field=True,
    )

    panels = [
        FieldPanel("navigation_links"),
    ]

    class Meta:
        verbose_name = "Navigacija"


@register_setting()
class FooterSettings(BaseGenericSetting):
    footer_links_left = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
            ("email_link", EmailLinkBlock()),
        ],
        verbose_name=_("Povezave v nogi na levi"),
        use_json_field=True,
    )
    footer_links_right = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
            ("email_link", EmailLinkBlock()),
        ],
        verbose_name=_("Povezave v nogi na desni"),
        use_json_field=True,
    )

    panels = [
        FieldPanel("footer_links_left"),
        FieldPanel("footer_links_right"),
    ]

    class Meta:
        verbose_name = "Footer"


@register_setting()
class SocialMedia(BaseGenericSetting):
    social_media_title_part_one = models.TextField(
        verbose_name="Naslov 1. del", blank=True
    )
    social_media_title_part_two = models.TextField(
        verbose_name="Naslov 2. del", blank=True
    )
    facebook_link = models.URLField(verbose_name="Facebook URL", blank=True, null=True)
    twitter_link = models.URLField(verbose_name="Twitter URL", blank=True, null=True)
    instagram_link = models.URLField(
        verbose_name="Instagram URL", blank=True, null=True
    )

    panels = [
        FieldPanel("social_media_title_part_one"),
        FieldPanel("social_media_title_part_two"),
        FieldPanel("facebook_link"),
        FieldPanel("twitter_link"),
        FieldPanel("instagram_link"),
    ]

    class Meta:
        verbose_name = "Družbena omrežja"


@register_setting()
class Newsletter(BaseGenericSetting):
    newsletter_title_part_one = models.TextField(
        verbose_name="Naslov 1. del", blank=True
    )
    newsletter_title_part_two = models.TextField(
        verbose_name="Naslov 2. del", blank=True
    )
    newsletter_email_label = models.TextField(
        verbose_name="Email naslov oznaka", blank=True
    )
    newsletter_terms = models.TextField(verbose_name="Novičnik pogoji", blank=True)
    newsletter_success = models.TextField(
        verbose_name="Sporočilo ob uspešni prijavi", blank=True
    )
    newsletter_failure = models.TextField(
        verbose_name="Sporočilo ob neuspešni prijavi", blank=True
    )

    panels = [
        FieldPanel("newsletter_title_part_one"),
        FieldPanel("newsletter_title_part_two"),
        FieldPanel("newsletter_email_label"),
        FieldPanel("newsletter_terms"),
        FieldPanel("newsletter_success"),
        FieldPanel("newsletter_failure"),
    ]

    class Meta:
        verbose_name = "Novičnik"


@register_setting()
class Support(BaseGenericSetting):
    support_title_part_one = models.TextField(verbose_name="Naslov 1. del", blank=True)
    support_title_part_two = models.TextField(verbose_name="Naslov 2. del", blank=True)
    support_text = models.TextField(verbose_name="Opis", blank=True)
    support_button = models.TextField(verbose_name="Besedilo na gumbu", blank=True)
    support_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Povezava",
    )

    panels = [
        FieldPanel("support_title_part_one"),
        FieldPanel("support_title_part_two"),
        FieldPanel("support_text"),
        FieldPanel("support_button"),
        FieldPanel("support_link"),
    ]

    class Meta:
        verbose_name = "Donacije"


@register_setting()
class Monitor(BaseGenericSetting):
    monitor_title_part_one = models.TextField(verbose_name="Naslov 1. del", blank=True)
    monitor_title_part_two = models.TextField(verbose_name="Naslov 2. del", blank=True)
    monitor_text = models.TextField(verbose_name="Opis", blank=True)
    monitor_button = models.TextField(verbose_name="Besedilo na gumbu", blank=True)
    monitor_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Povezava",
    )

    panels = [
        FieldPanel("monitor_title_part_one"),
        FieldPanel("monitor_title_part_two"),
        FieldPanel("monitor_text"),
        FieldPanel("monitor_button"),
        FieldPanel("monitor_link"),
    ]

    class Meta:
        verbose_name = "Prispevaj"


class Publication(models.Model):
    title = models.TextField()
    url = models.URLField()
    source = models.TextField()
    date = models.DateField()

    panels = [
        FieldPanel("title"),
        FieldPanel("url", classname="full"),
        FieldPanel("source"),
        FieldPanel("date"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Medijsko pojavljanje"
        verbose_name_plural = "Medijska pojavljanja"


class HomePage(Page):
    intro_text = RichTextField(
        blank=True,
        null=True,
        verbose_name="Uvodno besedilo",
    )
    intro_boxes = StreamField(
        [
            (
                "box",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock(label="Slika")),
                        ("text", blocks.CharBlock(label="Besedilo")),
                    ],
                    label="Kvadratek",
                ),
            ),
        ],
        verbose_name="Uvodni kvadratki",
        null=True,
        blank=True,
    )
    blog_section_title = models.TextField(
        verbose_name="Naslov blog sekcije", blank=True
    )
    blog_section_archive_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Povezava do seznama blog zapisov",
    )
    blog_section_archive_link_title = models.TextField(
        verbose_name="Ime povezave do seznama blog zapisov", blank=True
    )
    monitor_archive_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Povezava do seznama monitoring zapisov",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro_text", classname="full"),
        FieldPanel("intro_boxes"),
        FieldPanel("blog_section_title"),
        FieldPanel("blog_section_archive_link"),
        FieldPanel("blog_section_archive_link_title"),
        FieldPanel("monitor_archive_link"),
    ]

    parent_page_types = []

    def get_context(self, request):
        context = super().get_context(request)
        parent_page = self.blog_section_archive_link
        if not parent_page:
            blogposts = []
        else:
            blogposts = (
                BlogPage.objects.child_of(parent_page)
                .live()
                .order_by("-date", "-first_published_at", "id")[:6]
            )
        context["blogposts"] = blogposts
        return context

    class Meta:
        verbose_name = "Domača stran"
        verbose_name_plural = "Domače strani"


class GenericPage(Page):
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
    social_media_box = models.BooleanField(
        default=False, verbose_name="Škatla družbena omrežja"
    )
    newsletter_box = models.BooleanField(default=False, verbose_name="Škatla novičnik")
    support_box = models.BooleanField(default=False, verbose_name="Škatla podpri")
    monitor_box = models.BooleanField(default=False, verbose_name="Škatla prispevaj")

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
        FieldPanel("body"),
        FieldPanel("monitor_box"),
        FieldPanel("newsletter_box"),
        FieldPanel("social_media_box"),
        FieldPanel("support_box"),
    ]

    class Meta:
        verbose_name = "Generična stran"
        verbose_name_plural = "Generične strani"


class DonationPage(Page):
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    left_box_heading_part_one = models.TextField(
        blank=True, verbose_name="Leva škatla - naslov prvi del"
    )
    left_box_heading_part_two = models.TextField(
        blank=True, verbose_name="Leva škatla - naslov drugi del"
    )
    left_box_description = models.TextField(
        blank=True, verbose_name="Leva škatla - opis"
    )
    left_box_button_text = models.TextField(
        blank=True, verbose_name="Leva škatla - gumb besedilo"
    )
    left_box_button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Leva škatla - gumb povezava",
    )
    right_box_heading_part_one = models.TextField(
        blank=True, verbose_name="Desna škatla - naslov prvi del"
    )
    right_box_heading_part_two = models.TextField(
        blank=True, verbose_name="Desna škatla - naslov drugi del"
    )
    right_box_description = models.TextField(
        blank=True, verbose_name="Desna škatla - opis"
    )
    right_box_button_text = models.TextField(
        blank=True, verbose_name="Desna škatla - gumb besedilo"
    )
    right_box_button_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Desna škatla - gumb povezava",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("left_box_heading_part_one"),
        FieldPanel("left_box_heading_part_two"),
        FieldPanel("left_box_description"),
        FieldPanel("left_box_button_text"),
        FieldPanel("left_box_button_link"),
        FieldPanel("right_box_heading_part_one"),
        FieldPanel("right_box_heading_part_two"),
        FieldPanel("right_box_description"),
        FieldPanel("right_box_button_text"),
        FieldPanel("right_box_button_link"),
    ]

    class Meta:
        verbose_name = "Donacijska stran (z gumbi)"
        verbose_name_plural = "Donacijske strani (z gumbi)"


class DonationEmbedPage(Page):
    embed_url = models.URLField()

    content_panels = Page.content_panels + [
        FieldPanel("embed_url", classname="full"),
    ]

    class Meta:
        verbose_name = "Donacijska stran z embedom"
        verbose_name_plural = "Donacijske strani z embedom"
