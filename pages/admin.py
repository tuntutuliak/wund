from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "teacher", "start_date", "price")
    prepopulated_fields = {"slug": ("title",)}
