"""Context processors для приложения pages."""

from .forms import SubscribeForm, ApplicationForm


def subscribe_form(request):
    """Добавляет форму подписки на рассылку в контекст (для футера/секции подписки)."""
    return {"subscribe_form": SubscribeForm()}


def application_form(request):
    """Добавляет форму заявки в контекст (модальное окно «Оставить заявку»)."""
    return {"application_form": ApplicationForm()}
