from django.urls import path

from .views import BlogArchivePagedView

urlpatterns = [
    path(
        "blog-archive-paged/",
        BlogArchivePagedView.as_view(),
        name="blog_archive_paged_view",
    ),
]
