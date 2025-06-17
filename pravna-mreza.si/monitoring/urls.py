from django.urls import path

from .views import MonitoringArchivePagedView

urlpatterns = [
    path(
        "monitoring-archive-paged/",
        MonitoringArchivePagedView.as_view(),
        name="monitoring_archive_paged_view",
    ),
]
