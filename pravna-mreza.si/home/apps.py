from django.apps import AppConfig

from .patches import patch_wagtail_serve_view


class HomeConfig(AppConfig):
    name = "home"

    def ready(self):
        patch_wagtail_serve_view()
