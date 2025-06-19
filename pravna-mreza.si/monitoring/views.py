from django.http import Http404
from django.views.generic import TemplateView

from home.pagination import paginate_limit_offset

from .models import MonitoringArchivePage, MonitoringPage


class MonitoringArchivePagedView(TemplateView):
    template_name = "monitoring/monitoring_archive_paged_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parent = int(self.request.GET.get("parent", 0))
        parent_page = MonitoringArchivePage.objects.filter(pk=parent).first()
        if not parent_page:
            raise Http404("Parent page not found")

        offset = int(self.request.GET.get("offset", 0))
        all_monitoring_pages = (
            MonitoringPage.objects.child_of(parent_page)
            .live()
            .order_by("-date", "-first_published_at", "id")
        )
        context["monitoring_pages"] = paginate_limit_offset(
            all_monitoring_pages, limit=12, offset=offset
        )
        return context
