from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from home.models import EmailLinkBlock, ExternalLinkBlock, PageLinkBlock


class AchievementTag(models.Model):
    name = models.TextField(verbose_name="Oznaka dosežka", blank=True)

    def __str__(self):
        return self.name


class Achievement(models.Model):
    title = models.TextField(verbose_name="Naslov", blank=True)
    tag = models.ForeignKey(
        AchievementTag, on_delete=models.SET_NULL, null=True, blank=True
    )
    date2 = models.DateField(
        verbose_name="Začetni datum, če gre za obdobje (sicer naj ostane prazno)",
        null=True,
        blank=True,
    )
    date = models.DateField(verbose_name="Datum oz. končni datum, če gre za obdobje")
    description = models.TextField(verbose_name="Opis", blank=True)
    link = StreamField(
        [
            ("page_link", PageLinkBlock()),
            ("external_link", ExternalLinkBlock()),
            ("email_link", EmailLinkBlock()),
        ],
        null=True,
        blank=True,
        verbose_name="Povezava",
        use_json_field=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("tag"),
        FieldPanel("date2"),
        FieldPanel("date"),
        FieldPanel("description"),
        FieldPanel("link"),
    ]

    def __str__(self):
        return self.title


class AchievementArchivePage(Page):
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

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        achievements_by_year = {}

        # get all years
        date_list = Achievement.objects.all().dates("date", "year").order_by("-date")

        for year in date_list:
            achievements_by_year[year.year] = Achievement.objects.filter(
                date__year=year.year
            ).order_by("-date")

        context["achievements_by_year"] = achievements_by_year
        return context

    class Meta:
        verbose_name = "Stran z dosežki"
        verbose_name_plural = "Strani z dosežki"
