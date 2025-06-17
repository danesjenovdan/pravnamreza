from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page


class AboutUsPage(Page):
    headline_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Slika na naslovnici",
    )
    page_buttons = StreamField(
        [
            (
                "page",
                blocks.PageChooserBlock(
                    page_type=[
                        "achievements.AchievementArchivePage",
                        "mediapublications.MediaPublicationsPage",
                    ]
                ),
            ),
        ],
        null=True,
        blank=True,
        verbose_name="Gumbi s povezavami do strani",
    )
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
        ],
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline_image"),
        FieldPanel("page_buttons"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "O nas"
        verbose_name_plural = "O nas"
