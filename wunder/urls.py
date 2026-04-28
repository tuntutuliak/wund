from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from pages import views
from pages.sitemaps import build_sitemaps, sitemap_site
from wunder.admin_site import admin_site

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/img/favicon.ico", permanent=True),
        name="favicon",
    ),
    path("subscribe/", views.subscribe_view, name="subscribe"),
    path("subscribe/confirm/<uuid:token>/", views.confirm_subscription_view, name="confirm_subscription"),
    path("application/submit/", views.application_submit_view, name="application_submit"),
    path("admin/", admin_site.urls),
    path("", views.home, name="home"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("team/", views.team, name="team"),
    path("teachers/", views.teachers_catalog, name="teachers_catalog"),
    path("programs/", views.programms, name="programs"),
    path("programms/<slug:slug>/", views.course_detail, name="course_detail"),
    path("organization/", RedirectView.as_view(url="/contacts/", permanent=True), name="organization"),
    path("svedeniya/", RedirectView.as_view(url="/contacts/", permanent=True)),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("news/", views.news_list, name="news"),
    path("events/", views.events, name="events"),
    path("group-course/", views.group_course, name="group_course"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": build_sitemaps(), "site": sitemap_site(), "protocol": "https"},
        name="sitemap",
    ),
]

# Локальная разработка: раздача медиа (изображения новостей и т.д.) по /media/
if settings.DEBUG and getattr(settings, "MEDIA_ROOT", None):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
