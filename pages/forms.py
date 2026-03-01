from django import forms
from django.core.exceptions import ValidationError

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    """Форма подписки на рассылку с honeypot и проверкой дубликатов."""

    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
        label="",
    )

    class Meta:
        model = Subscriber
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "id": "subscribe-form-email",
                    "placeholder": "Ваш e-mail",
                    "autocomplete": "email",
                    "aria-label": "Ваш e-mail",
                }
            ),
        }
        labels = {"email": "Ваш e-mail"}
        error_messages = {"email": {"invalid": "Введите корректный e-mail адрес."}}

    def clean_website(self):
        """Honeypot: если заполнено — бот (view вернёт фейковый успех, не сохраняя)."""
        return (self.cleaned_data.get("website") or "").strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email
        email = email.lower().strip()
        try:
            existing = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            return email
        if existing.is_active:
            raise ValidationError("Вы уже подписаны на рассылку.")
        return email
