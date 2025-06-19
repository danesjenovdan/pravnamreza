from django.views.generic import TemplateView

from home.pagination import paginate_limit_offset

from .models import BlogPage, BlogTag


class BlogArchivePagedView(TemplateView):
    template_name = "blog/blog_archive_paged_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offset = int(self.request.GET.get("offset", 0))

        tags = BlogTag.objects.all().order_by("name")
        context["tags"] = tags

        selected_tag = None
        slug_to_tag = {tag.slug: tag for tag in tags}
        if tag_slug := self.request.GET.get("tag", None):
            selected_tag = slug_to_tag.get(tag_slug, None)
        context["selected_tag"] = selected_tag

        all_blogposts = (
            BlogPage.objects.all().live().order_by("-date", "-first_published_at", "id")
        )
        if selected_tag:
            all_blogposts = all_blogposts.filter(tag=selected_tag)
        context["blogposts"] = paginate_limit_offset(
            all_blogposts, limit=12, offset=offset
        )
        return context
