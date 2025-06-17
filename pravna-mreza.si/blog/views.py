from django.views.generic import TemplateView

from home.pagination import paginate_limit_offset

from .models import BlogPage


class BlogArchivePagedView(TemplateView):
    template_name = "blog/blog_archive_paged_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offset = int(self.request.GET.get("offset", 0))
        all_blogposts = (
            BlogPage.objects.all().live().order_by("-date", "-first_published_at", "id")
        )
        context["blogposts"] = paginate_limit_offset(
            all_blogposts, limit=12, offset=offset
        )
        return context
