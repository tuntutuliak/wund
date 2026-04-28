from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import News, Course


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return [
            "home",
            "about",
            "programs",
            "teachers_catalog",
            "news",
            "events",
            "contacts",
            "privacy",
            "terms",
            "team",
            "group_course",
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return News.objects.filter(is_published=True).order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at


class CourseSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return Course.objects.all()

    def location(self, obj):
        return reverse("course_detail", kwargs={"slug": obj.slug})


def build_sitemaps():
    return {
        "static": StaticViewSitemap,
        "news": NewsSitemap,
        "courses": CourseSitemap,
    }


class _Site:
    def __init__(self, domain: str):
        self.domain = domain
        self.name = domain


def sitemap_site():
    site_url = getattr(settings, "SITE_URL", "https://wunder.education").rstrip("/")
    domain = site_url.split("://", 1)[-1]
    return _Site(domain=domain)

