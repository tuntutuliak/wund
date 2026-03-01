from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from pages import views
from wunder.admin_site import admin_site

urlpatterns = [
    path("admin/", admin_site.urls),
    path("", views.home, name="home"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("teachers/", views.team, name="team"),
    path("programs/", views.programms, name="programms"),
    path("programms/<slug:slug>/", views.course_detail, name="course_detail"),
    path("svedeniya/", RedirectView.as_view(url="/contacts/", permanent=True)),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
    path("news/", views.news_list, name="news"),
    path("events/", views.events, name="events"),
    path("group-course/", views.group_course, name="group_course"),
]

# Локальная разработка: раздача медиа (изображения новостей и т.д.) по /media/
if settings.DEBUG and getattr(settings, "MEDIA_ROOT", None):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
