from django import template

from home.models import Infopush

register = template.Library()


# Infopush snippets
@register.inclusion_tag("home/tags/infopush.html", takes_context=True)
def infopush(context):
    return {
        "infopushes": Infopush.objects.all().order_by("-id"),
        "request": context["request"],
    }
