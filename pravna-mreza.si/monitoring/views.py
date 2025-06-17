from django.views.generic import TemplateView

from home.pagination import paginate_limit_offset

from .models import MonitoringPage


class MonitoringArchivePagedView(TemplateView):
    template_name = "monitoring/monitoring_archive_paged_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offset = int(self.request.GET.get("offset", 0))
        all_monitoring_pages = (
            MonitoringPage.objects.all()
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        context["monitoring_pages"] = paginate_limit_offset(
            all_monitoring_pages, limit=12, offset=offset
        )
        return context
