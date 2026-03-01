"""Context processors для приложения pages."""

from .forms import SubscribeForm


def subscribe_form(request):
    """Добавляет форму подписки на рассылку в контекст (для футера/секции подписки)."""
    return {"subscribe_form": SubscribeForm()}
