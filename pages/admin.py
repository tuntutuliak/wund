from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Course, News

User._meta.verbose_name = "Пользователь"
User._meta.verbose_name_plural = "Пользователи"
Group._meta.verbose_name = "Группа"
Group._meta.verbose_name_plural = "Группы"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "teacher", "start_date", "price")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "created_at")
    search_fields = ("title", "short_description", "content")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
