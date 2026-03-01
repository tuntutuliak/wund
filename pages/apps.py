from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    verbose_name = "Контент"

    def ready(self):
        # Русское название блока «Пользователи и группы» в админке (без изменения ядра Django)
        from django.apps import apps
        auth_config = apps.get_app_config("auth")
        auth_config.verbose_name = "Пользователи и группы"
