from django.views.generic import TemplateView

from home.models import Publication
from home.pagination import paginate_limit_offset


class MediaPublicationsPagedView(TemplateView):
    template_name = "mediapublications/media_publications_paged_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offset = int(self.request.GET.get("offset", 0))
        all_publications = Publication.objects.all().order_by("-date", "id")
        context["publications"] = paginate_limit_offset(
            all_publications, limit=12, offset=offset
        )
        return context
