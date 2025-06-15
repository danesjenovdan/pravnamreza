from django.core.management.base import BaseCommand, CommandError

from blog.models import BlogArchivePage, BlogPage, BlogTag
from monitoring.models import MonitoringArchivePage, MonitoringPage
from novice.models import NovicaArchivePage, NovicaPage, NovicaTag


class Command(BaseCommand):
    help = "Migrate news to blog posts and move them under the archive page."

    def _rename_blog_archive_page(self):
        self.stdout.write(self.style.WARNING("Renaming BlogArchivePage..."))
        archive_pages = BlogArchivePage.objects.all()
        if not archive_pages:
            raise CommandError("No BlogArchivePage found.")
        if len(archive_pages) > 1:
            raise CommandError("Multiple BlogArchivePage instances found.")

        archive_page = archive_pages.first()
        archive_page.title = "Objave"
        archive_page.slug = "objave"
        archive_page.save_revision().publish()

        self.stdout.write(
            self.style.SUCCESS("BlogArchivePage renamed to 'Objave'."),
            ending="\n\n",
        )

    def _migrate_news_tags_to_blog_tags(self):
        self.stdout.write(self.style.WARNING("Migrating news tags to blog tags..."))
        news_tags = NovicaTag.objects.all()
        for tag in news_tags:
            tag_print = self.style.WARNING(f"{tag.name[:50]}")
            blog_tag, created = BlogTag.objects.get_or_create(name=tag.name)
            if created:
                self.stdout.write(f"Created new BlogTag: {tag_print}")
            else:
                self.stdout.write(f"BlogTag already exists: {tag_print}")
        self.stdout.write(
            self.style.SUCCESS("All news tags migrated to blog tags."),
            ending="\n\n",
        )

    def _migrate_blog_pages_under_archive_page(self):
        self.stdout.write(
            self.style.WARNING("Migrating blog pages under archive page...")
        )
        archive_page = BlogArchivePage.objects.first()
        if not archive_page:
            raise CommandError("No BlogArchivePage found.")

        blog_pages = BlogPage.objects.all()
        for blog_page in blog_pages:
            page_url_parts = blog_page.get_url_parts()
            page_path = page_url_parts[2] if page_url_parts else None

            title_print = self.style.WARNING(f"{blog_page.title[:50]}")
            if blog_page.get_parent().id == archive_page.id:
                self.stdout.write(f"BlogPage already in place: {title_print}")
            elif blog_page.live:
                self.stdout.write(f"Moving BlogPage: {title_print}")
                blog_page.old_migrated_page_path = page_path
                blog_page.save()
                blog_page.move(archive_page, pos="last-child")

        BlogPage.objects.filter(live=False).delete()

        self.stdout.write(
            self.style.SUCCESS("All blog pages migrated under the archive page."),
            ending="\n\n",
        )

    def _migrate_news_pages_to_blog_pages(self):
        self.stdout.write(self.style.WARNING("Migrating news pages to blog pages..."))
        archive_page = BlogArchivePage.objects.first()
        if not archive_page:
            raise CommandError("No BlogArchivePage found.")

        news_pages = NovicaPage.objects.all()
        for news_page in news_pages:
            page_url_parts = news_page.get_url_parts()
            page_path = page_url_parts[2] if page_url_parts else None

            title_print = self.style.WARNING(f"{news_page.title[:50]}")
            if (
                page_path
                and BlogPage.objects.filter(old_migrated_page_path=page_path).exists()
            ):
                self.stdout.write(f"BlogPage already exists: {title_print}")
            elif news_page.live:
                self.stdout.write(f"Creating BlogPage: {title_print}")

                slug_suffix_number = 1
                slug_suffix = ""
                while (
                    archive_page.get_children()
                    .filter(slug=f"{news_page.slug}{slug_suffix}")
                    .exists()
                ):
                    slug_suffix_number += 1
                    slug_suffix = f"-{slug_suffix_number}"
                slug = f"{news_page.slug}{slug_suffix}"

                blog_page = BlogPage(
                    title=news_page.title,
                    date=news_page.date,
                    preview_text=news_page.preview_text,
                    preview_image=news_page.preview_image,
                    intro_text=news_page.intro_text,
                    body=news_page.body,
                    meta_image=news_page.meta_image,
                    #
                    old_migrated_page_path=page_path,
                    #
                    slug=slug,
                    live=news_page.live,
                    first_published_at=news_page.first_published_at,
                    last_published_at=news_page.last_published_at,
                    locale=news_page.locale,
                )

                if news_page.tag:
                    blog_tag = BlogTag.objects.filter(name=news_page.tag.name).first()
                    blog_page.tag = blog_tag

                archive_page.add_child(instance=blog_page)
                blog_page.save_revision().publish()

        NovicaPage.objects.all().delete()
        NovicaArchivePage.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS("All news pages migrated to blog pages."),
            ending="\n\n",
        )

    def _migrate_monitoring_pages_under_archive_page(self):
        self.stdout.write(
            self.style.WARNING("Migrating monitoring pages under archive page...")
        )
        archive_page = MonitoringArchivePage.objects.first()
        if not archive_page:
            raise CommandError("No MonitoringArchivePage found.")

        monitoring_pages = MonitoringPage.objects.all()
        for monitoring_page in monitoring_pages:
            page_url_parts = monitoring_page.get_url_parts()
            page_path = page_url_parts[2] if page_url_parts else None

            title_print = self.style.WARNING(f"{monitoring_page.title[:50]}")
            if monitoring_page.get_parent().id == archive_page.id:
                self.stdout.write(f"MonitoringPage already in place: {title_print}")
            elif monitoring_page.live:
                self.stdout.write(f"Moving MonitoringPage: {title_print}")
                monitoring_page.old_migrated_page_path = page_path
                monitoring_page.save()
                monitoring_page.move(archive_page, pos="last-child")

        MonitoringPage.objects.filter(live=False).delete()

        self.stdout.write(
            self.style.SUCCESS("All monitoring pages migrated under the archive page."),
            ending="\n\n",
        )

    def handle(self, *args, **options):
        self._rename_blog_archive_page()
        self._migrate_news_tags_to_blog_tags()
        self._migrate_blog_pages_under_archive_page()
        self._migrate_news_pages_to_blog_pages()
        self._migrate_monitoring_pages_under_archive_page()
        self.stdout.write(self.style.SUCCESS("Migration complete."))
