from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Course, News, Teacher, ContactSection, ContactDocument, Subscriber

try:
    from ckeditor.widgets import CKEditorWidget
except ImportError:
    CKEditorWidget = None

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


class ContactDocumentInline(admin.TabularInline):
    model = ContactDocument
    extra = 0
    fields = ("name", "file")


class ContactSectionAdminForm(forms.ModelForm):
    class Meta:
        model = ContactSection
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if CKEditorWidget is not None:
            self.fields["content"].widget = CKEditorWidget()


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    form = ContactSectionAdminForm
    list_display = ("order", "title")
    list_editable = ("order",)
    list_display_links = ("title",)
    search_fields = ("title",)
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = ((None, {"fields": ("title", "slug", "order", "content")}),)
    inlines = [ContactDocumentInline]


@admin.register(ContactDocument)
class ContactDocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "section")
    list_filter = ("section",)
    search_fields = ("name",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at", "confirmed_at")
    search_fields = ("email",)
    list_filter = ("is_active", "created_at")
    readonly_fields = ("confirmation_token", "created_at", "confirmed_at", "ip_address", "user_agent")
