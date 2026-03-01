"""
Кастомный AdminSite: заголовки, главная с двумя блоками (Контент, Пользователи и группы).
Модели регистрируются здесь, чтобы использовать этот site вместо стандартного.
"""
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.template.response import TemplateResponse


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
        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            "app_groups": app_groups,
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
from pages.models import Course, News  # noqa: E402

admin.site.unregister(Course)
admin.site.unregister(News)
admin_site.register(Course, pages_admin_module.CourseAdmin)
admin_site.register(News, pages_admin_module.NewsAdmin)
