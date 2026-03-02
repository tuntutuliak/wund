from django import forms
from django.core.exceptions import ValidationError

from .models import Subscriber, Application, GroupCourseRequest


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


class ApplicationForm(forms.ModelForm):
    """Форма заявки (модальное окно «Оставить заявку»)."""

    class Meta:
        model = Application
        fields = ("name", "phone", "email", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "application-form-input", "placeholder": "Введите имя", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"class": "application-form-input", "placeholder": "Введите телефон", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"class": "application-form-input", "placeholder": "Введите e-mail", "autocomplete": "email"}),
            "message": forms.Textarea(attrs={"class": "application-form-input", "placeholder": "Введите сообщение", "rows": 4}),
        }
        labels = {"name": "Имя", "phone": "Телефон", "email": "E-mail", "message": "Сообщение"}
        error_messages = {
            "name": {"required": "Укажите имя."},
            "phone": {"required": "Укажите телефон."},
            "email": {"required": "Укажите e-mail.", "invalid": "Введите корректный e-mail."},
        }

    def clean_phone(self):
        value = (self.cleaned_data.get("phone") or "").strip()
        if not value:
            raise ValidationError("Укажите телефон.")
        return value

    def clean_name(self):
        value = (self.cleaned_data.get("name") or "").strip()
        if not value:
            raise ValidationError("Укажите имя.")
        return value


GROUP_COURSE_INITIAL = {
    "preferred_start_date": "",
    "group_type": "mini",
    "level": "beginner",
    "schedule": "2_per_week",
}


class GroupCourseRequestForm(forms.ModelForm):
    class Meta:
        model = GroupCourseRequest
        fields = ("preferred_start_date", "group_type", "level", "schedule", "name", "phone", "email")
        widgets = {
            "preferred_start_date": forms.TextInput(
                attrs={
                    "class": "form-input select2-input-gray",
                    "placeholder": "Дата начала",
                    "data-minimum-results-for-search": "Infinity",
                    "data-container-class": "input-gray",
                }
            ),
            "group_type": forms.Select(
                attrs={
                    "class": "form-input select",
                    "data-minimum-results-for-search": "Infinity",
                    "data-container-class": "select-gray",
                    "data-dropdown-class": "select-gray",
                }
            ),
            "level": forms.Select(
                attrs={
                    "class": "form-input select",
                    "data-minimum-results-for-search": "Infinity",
                    "data-container-class": "select-gray",
                    "data-dropdown-class": "select-gray",
                }
            ),
            "schedule": forms.Select(
                attrs={
                    "class": "form-input select",
                    "data-minimum-results-for-search": "Infinity",
                    "data-container-class": "select-gray",
                    "data-dropdown-class": "select-gray",
                }
            ),
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Имя"}),
            "phone": forms.TextInput(attrs={"class": "form-input", "placeholder": "Телефон"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "E-mail"}),
        }
        labels = {
            "preferred_start_date": "",
            "group_type": "",
            "level": "",
            "schedule": "",
            "name": "Имя",
            "phone": "Телефон",
            "email": "E-mail",
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("initial", {}).update(GROUP_COURSE_INITIAL)
        super().__init__(*args, **kwargs)
        self.fields["group_type"].choices = [
            ("mini", "Мини-группа (до 6 человек)"),
            ("standard", "Стандартная группа"),
            ("intensive", "Интенсив"),
        ]
        self.fields["level"].choices = [
            ("beginner", "Начальный"),
            ("intermediate", "Средний"),
            ("advanced", "Продвинутый"),
        ]
        self.fields["schedule"].choices = [
            ("2_per_week", "2 раза в неделю"),
            ("3_per_week", "3 раза в неделю"),
            ("daily", "Интенсив (ежедневно)"),
        ]
        self.fields["group_type"].required = True
        self.fields["level"].required = True
        self.fields["schedule"].required = True
