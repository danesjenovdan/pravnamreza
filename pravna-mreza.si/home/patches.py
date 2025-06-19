from django.http import Http404
from django.shortcuts import redirect


def patch_wagtail_serve_view():
    """
    Patch the Wagtail serve view to handle redirects from migrated pages.
    """
    from wagtail import views

    original_serve = views.serve

    def patched_serve(request, *args, **kwargs):
        try:
            return original_serve(request, *args, **kwargs)
        except Http404:
            print(f"Page not found with path: {request.path}")

            from blog.models import BlogPage
            from monitoring.models import MonitoringPage

            if migrated_page := BlogPage.objects.filter(
                old_migrated_page_path=request.path
            ).first():
                print(f"Redirecting to migrated blog page: {migrated_page.url}")
                return redirect(
                    migrated_page.url,
                    permanent=True,
                )

            if migrated_page := MonitoringPage.objects.filter(
                old_migrated_page_path=request.path
            ).first():
                print(f"Redirecting to migrated monitoring page: {migrated_page.url}")
                return redirect(
                    migrated_page.url,
                    permanent=True,
                )

        raise Http404

    views.serve = patched_serve
