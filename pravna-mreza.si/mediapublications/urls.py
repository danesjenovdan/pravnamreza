from django.urls import path

from .views import MediaPublicationsPagedView

urlpatterns = [
    path(
        "media-publications-paged/",
        MediaPublicationsPagedView.as_view(),
        name="media_publications_paged_view",
    ),
]
