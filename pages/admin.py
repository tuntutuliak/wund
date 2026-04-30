import os
import shutil
import subprocess
import tempfile

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.files.base import File

from .models import Course, News, Teacher, ContactSection, ContactDocument, Subscriber, Application, GroupCourseRequest

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


def _is_probably_pdf(uploaded_file) -> bool:
    """
    Определяем PDF максимально дёшево и безопасно.
    Не полагаемся только на расширение/Content-Type.
    """
    name = (getattr(uploaded_file, "name", "") or "").lower()
    if name.endswith(".pdf"):
        return True
    try:
        f = uploaded_file.file  # Django UploadedFile
        pos = f.tell()
        head = f.read(5)
        f.seek(pos)
        return head == b"%PDF-"
    except Exception:
        return False


def _optimize_pdf_with_ghostscript(uploaded_file, *, pdfsettings: str = "/ebook", timeout_s: int = 180):
    """
    Сжимает загруженный PDF с помощью Ghostscript (gs) во временную папку.

    - Если gs не установлен или команда завершилась ошибкой → возвращаем None (сохраняем оригинал).
    - Пишем input через chunks() (не грузим файл целиком в память) — безопасно для 50MB+.
    - Вызываем Ghostscript в безопасном режиме: -dSAFER.
    """
    gs = shutil.which("gs")
    if not gs:
        return None

    in_path = None
    out_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix="upload_", suffix=".pdf", delete=False) as in_tmp:
            in_path = in_tmp.name
            for chunk in uploaded_file.chunks():
                in_tmp.write(chunk)

        out_fd, out_path = tempfile.mkstemp(prefix="optimized_", suffix=".pdf")
        os.close(out_fd)

        cmd = [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={pdfsettings}",
            "-dNOPAUSE",
            "-dBATCH",
            "-dSAFER",
            "-dDetectDuplicateImages=true",
            "-dCompressFonts=true",
            "-dSubsetFonts=true",
            f"-sOutputFile={out_path}",
            in_path,
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout_s,
        )

        if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
            return None

        return out_path
    except Exception:
        return None
    finally:
        if in_path and os.path.exists(in_path):
            try:
                os.remove(in_path)
            except OSError:
                pass


class ContactDocumentAdminForm(forms.ModelForm):
    """
    Админ-форма для ContactDocument.

    Цель: если загружают PDF через Django admin, автоматически сжимаем его
    ДО сохранения в storage (MEDIA_ROOT) с профилем Ghostscript /ebook.
    """

    class Meta:
        model = ContactDocument
        fields = "__all__"

    def save(self, commit=True):
        uploaded = self.files.get("file")
        optimized_path = None
        optimized_fp = None

        # Обрабатываем только новый загруженный файл (если поле не меняли — self.files пустой).
        if uploaded and _is_probably_pdf(uploaded):
            optimized_path = _optimize_pdf_with_ghostscript(uploaded, pdfsettings="/ebook")
            if optimized_path:
                optimized_fp = open(optimized_path, "rb")
                # Дадим Django файловый объект; storage сам скопирует в MEDIA_ROOT.
                self.instance.file = File(optimized_fp, name=uploaded.name)

        try:
            return super().save(commit=commit)
        finally:
            # Чистим временные файлы после фактического сохранения.
            if optimized_fp:
                try:
                    optimized_fp.close()
                except Exception:
                    pass
            if optimized_path and os.path.exists(optimized_path):
                try:
                    os.remove(optimized_path)
                except OSError:
                    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "teacher", "start_date", "price", "created_at")
    list_filter = ("is_active", "start_date", "created_at")
    search_fields = ("title", "subtitle", "description", "teacher")
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
    form = ContactDocumentAdminForm


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
    form = ContactDocumentAdminForm
    list_display = ("name", "section")
    list_filter = ("section",)
    search_fields = ("name",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "created_at", "confirmed_at")
    search_fields = ("email",)
    list_filter = ("is_active", "created_at")
    readonly_fields = ("confirmation_token", "created_at", "confirmed_at", "ip_address", "user_agent")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone", "message")
    list_filter = ("created_at",)
    readonly_fields = ("name", "phone", "email", "message", "created_at")
    fieldsets = (
        (None, {"fields": ("name", "phone", "email", "message", "created_at")}),
    )
    list_display_links = ("name", "email")

    def has_delete_permission(self, request, obj=None):
        """Заявки не удаляются из админки."""
        return False


@admin.register(GroupCourseRequest)
class GroupCourseRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "group_type", "level", "schedule", "preferred_start_date", "created_at", "processed")
    list_filter = ("group_type", "level", "schedule", "processed", "created_at")
    search_fields = ("name", "phone", "email")
