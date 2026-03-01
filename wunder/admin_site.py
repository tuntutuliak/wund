"""
Кастомный AdminSite: заголовки, дашборд со статистикой и блоками (Контент, Пользователи и группы).
"""
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.template.response import TemplateResponse
from django.urls import NoReverseMatch, reverse


class WunderAdminSite(admin.AdminSite):
    site_header = "Администрирование сайта"
    site_title = "Панель управления"
    index_title = "Управление контентом"
    index_template = "admin/index.html"

    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)
        content_apps = [a for a in app_list if a["app_label"] == "pages"]
        auth_apps = [a for a in app_list if a["app_label"] == "auth"]
        app_groups = [
            {"name": "Контент", "apps": content_apps},
            {"name": "Пользователи и группы", "apps": auth_apps},
        ]

        # Статистика для дашборда
        from django.contrib.auth import get_user_model
        from pages.models import Course, News

        User = get_user_model()
        dashboard_stats = {
            "news_count": News.objects.count(),
            "news_published_count": News.objects.filter(is_published=True).count(),
            "courses_count": Course.objects.count(),
            "users_count": User.objects.count(),
        }

        # URL для быстрых действий
        def _url(name):
            try:
                return reverse(name, current_app=self.name)
            except NoReverseMatch:
                return None

        quick_actions = {
            "add_news_url": _url("admin:pages_news_add"),
            "add_course_url": _url("admin:pages_course_add"),
            "view_site_url": "/",
        }

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            "app_groups": app_groups,
            "dashboard_stats": dashboard_stats,
            "quick_actions": quick_actions,
            **(extra_context or {}),
        }
        request.current_app = self.name
        return TemplateResponse(request, self.index_template, context)


# Единственный экземпляр кастомной админки
admin_site = WunderAdminSite(name="admin")

# Регистрация моделей auth
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Регистрация моделей pages (снять с default site и повесить на наш)
import pages.admin as pages_admin_module  # noqa: E402
from pages.models import Course, News, Teacher, EducationSection, ContactSection, ContactDocument  # noqa: E402

admin.site.unregister(Course)
admin.site.unregister(News)
admin.site.unregister(Teacher)
admin.site.unregister(EducationSection)
admin.site.unregister(ContactSection)
admin.site.unregister(ContactDocument)
admin_site.register(Course, pages_admin_module.CourseAdmin)
admin_site.register(News, pages_admin_module.NewsAdmin)
admin_site.register(Teacher, pages_admin_module.TeacherAdmin)
admin_site.register(EducationSection, pages_admin_module.EducationSectionAdmin)
admin_site.register(ContactSection, pages_admin_module.ContactSectionAdmin)
admin_site.register(ContactDocument, pages_admin_module.ContactDocumentAdmin)
