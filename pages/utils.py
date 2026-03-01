"""Утилиты для приложения pages."""


def get_client_ip(request):
    """Извлечь IP клиента с учётом прокси (X-Forwarded-For, X-Real-IP)."""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")
