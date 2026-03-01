from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Course, News, Teacher

User._meta.verbose_name = "Пользователь"
User._meta.verbose_name_plural = "Пользователи"
Group._meta.verbose_name = "Группа"
Group._meta.verbose_name_plural = "Группы"

# Fallback для превью в админке, если у новости нет изображения
ADMIN_NEWS_IMAGE_FALLBACK = static("img/ai_570x352.jpg")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "teacher", "start_date", "price")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "title", "slug", "is_published", "created_at")
    search_fields = ("title", "short_description", "content")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("image_thumbnail",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "short_description", "content", "image", "image_thumbnail", "is_published")}),
    )

    def image_preview(self, obj):
        url = obj.image.url if obj.image else ADMIN_NEWS_IMAGE_FALLBACK
        return format_html(
            '<img src="{}" alt="" style="max-width:80px;max-height:50px;object-fit:cover;" />',
            url,
        )

    image_preview.short_description = "Превью"

    def image_thumbnail(self, obj):
        url = obj.image.url if obj.image else ADMIN_NEWS_IMAGE_FALLBACK
        return format_html(
            '<img src="{}" alt="" style="max-width:300px;max-height:200px;object-fit:contain;" />',
            url,
        )

    image_thumbnail.short_description = "Изображение"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subject", "is_active")
    list_filter = ("is_active",)
    search_fields = ("full_name", "subject")
