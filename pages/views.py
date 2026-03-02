import logging
import time
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import News, Teacher, ContactSection, Subscriber, Application
from .forms import SubscribeForm, ApplicationForm
from .utils import get_client_ip

logger = logging.getLogger(__name__)

SUBSCRIBE_RATE_LIMIT_SECONDS = 60
APPLICATION_RATE_LIMIT_SECONDS = 60

# MOCK DATA – replace with real database later
MOCK_COURSES = [
    {
        "title": "Подготовка к ЕГЭ по математике",
        "slug": "ege-matematika",
        "subtitle": "Системный курс подготовки к профильному ЕГЭ по математике.",
        "image": "images/grid-blog-1-570x352.jpg",
        "description": "<p>Разбор заданий, пробные экзамены и сопровождение до дня экзамена. Курс рассчитан на учеников 10–11 классов.</p><p>Занятия проходят в мини-группах, возможна индивидуальная подготовка.</p>",
        "teacher": "Образовательный центр",
        "start_date": "15.03.2025",
        "duration": "8 месяцев",
        "price": "от 6 000 ₽/мес",
    },
    {
        "title": "Подготовка к ЕГЭ по русскому языку",
        "slug": "ege-russkij",
        "subtitle": "Работа с текстом и сочинением, подготовка к итоговому сочинению и ЕГЭ.",
        "image": "images/grid-blog-2-570x352.jpg",
        "description": "<p>Подготовка к итоговому сочинению и ЕГЭ по русскому языку. Разбор критериев, тренировка заданий и письменных работ.</p>",
        "teacher": "Образовательный центр",
        "start_date": "01.04.2025",
        "duration": "7 месяцев",
        "price": "от 5 500 ₽/мес",
    },
    {
        "title": "Углублённый курс английского языка",
        "slug": "anglijskij",
        "subtitle": "Коммуникативная методика, подготовка к ОГЭ и ЕГЭ, разговорный английский.",
        "image": "images/grid-blog-3-570x352.jpg",
        "description": "<p>Практика с носителями, подготовка к ОГЭ и ЕГЭ. Программа для 7–11 классов.</p>",
        "teacher": "Образовательный центр",
        "start_date": "10.02.2025",
        "duration": "9 месяцев",
        "price": "от 7 000 ₽/мес",
    },
    {
        "title": "Курс программирования для школьников",
        "slug": "programmirovanie",
        "subtitle": "Основы алгоритмов и программирования на Python, олимпиады и проекты.",
        "image": "images/grid-blog-4-570x352.jpg",
        "description": "<p>Подготовка к олимпиадам и проектная работа. Курс для 7–10 классов.</p>",
        "teacher": "Образовательный центр",
        "start_date": "20.02.2025",
        "duration": "6 месяцев",
        "price": "от 6 500 ₽/мес",
    },
]


def _get_mock_contact_sections():
    """Mock sections for contacts page when DB has none (for preview)."""
    from types import SimpleNamespace
    return [
        SimpleNamespace(
            slug="osnovnye-svedeniya",
            title="Основные сведения",
            content=(
                "<h3>Местонахождение</h3>"
                "<p>Юридический адрес: 690911, Приморский край, г. Владивосток, ул. Адмирала Горшкова, д.52.</p>"
                "<h3>Контакты</h3>"
                "<p>Адрес электронной почты: info@wunder.education</p>"
                "<p>Телефон: +7 (902) 506-74-44</p>"
                "<p>График работы: Пн–Пт 8:00–20:00, Сб 8:00–18:00</p>"
            ),
            documents=[],
        ),
        SimpleNamespace(
            slug="struktura-i-organy-upravleniya",
            title="Структура и органы управления образовательной организацией",
            content=(
                "<p><strong>Наименование:</strong> старшая школа</p>"
                "<p><strong>Руководитель:</strong> директор, Ермак Анна Владимировна</p>"
                "<p><strong>Адрес:</strong> 690100, г. Владивосток, Океанский проспект 101А, оф.18-34</p>"
                "<p><strong>Сайт:</strong> wunder.education</p>"
            ),
            documents=[],
        ),
        SimpleNamespace(
            slug="dokumenty",
            title="Документы",
            content=(
                "<p>Сведения о государственной регистрации и лицензии. "
                "Документы можно загрузить в разделе «Документы» в админ-панели.</p>"
            ),
            documents=[],
        ),
    ]


def home(request):
    """Главная страница — рендер base.html с контентом по умолчанию."""
    return render(request, 'base.html')


def testimonials(request):
    """Страница отзывов — та же функциональность, что и school-site/templates/testimonials.html."""
    return render(request, 'testimonials.html')


def about(request):
    """Страница «О нас»."""
    return render(request, 'about.html')


def contacts_view(request):
    """Контакты и сведения об образовательной организации — разделы из БД или mock."""
    sections = list(ContactSection.objects.all().order_by("order").prefetch_related("documents"))
    if not sections:
        sections = _get_mock_contact_sections()
    # Unified .documents_list for template (real sections have .documents, mock have .documents)
    for s in sections:
        if hasattr(s, "documents") and hasattr(s.documents, "all"):
            s.documents_list = list(s.documents.all())
        else:
            s.documents_list = getattr(s, "documents", [])
    return render(request, "contacts.html", {"sections": sections})


def team(request):
    """Страница-раздел «Преподаватели» (руководство и блок с кнопкой в каталог)."""
    return render(request, "team.html")


def teachers_catalog(request):
    """Каталог преподавателей: сетка карточек, только is_active=True."""
    teachers = Teacher.objects.filter(is_active=True)
    return render(request, "teachers/catalog.html", {"teachers": teachers})


def programms(request):
    """Страница «Программы» (MOCK: список из MOCK_COURSES). GET ?program=slug для фильтра/подсветки."""
    program_slug = request.GET.get('program', '').strip()
    return render(request, 'programms.html', {
        'courses': MOCK_COURSES,
        'program_filter': program_slug,
    })


def course_detail(request, slug):
    """Страница курса по slug (MOCK: поиск в MOCK_COURSES)."""
    course = next((c for c in MOCK_COURSES if c['slug'] == slug), None)
    if course is None:
        raise Http404()
    return render(request, 'single_course.html', {'course': course})


def news_list(request):
    """Список опубликованных новостей."""
    news_list_qs = News.objects.filter(is_published=True)
    return render(request, "news.html", {"news_list": news_list_qs})


def news_detail(request, slug):
    """Страница одной новости по slug. 404 если не найдена или не опубликована."""
    news = get_object_or_404(News, slug=slug, is_published=True)
    return render(request, 'single_news.html', {'news': news})


def events(request):
    return render(request, 'events.html')


def group_course(request):
    from django.shortcuts import redirect
    from .forms import GroupCourseRequestForm, GROUP_COURSE_INITIAL
    if request.method == "POST":
        form = GroupCourseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("group_course") + "?success=1")
    else:
        form = GroupCourseRequestForm(initial=GROUP_COURSE_INITIAL)
    return render(request, "group_course.html", {"form": form, "success": request.GET.get("success") == "1"})


def _check_subscribe_rate_limit(request):
    """Session-based rate limit: один запрос подписки в SUBSCRIBE_RATE_LIMIT_SECONDS."""
    key = "subscribe_last_attempt"
    now = time.time()
    last = request.session.get(key)
    if last is not None and (now - last) < SUBSCRIBE_RATE_LIMIT_SECONDS:
        return False
    request.session[key] = now
    return True


@require_http_methods(["POST"])
def subscribe_view(request):
    """POST: принять подписку, сохранить в БД, отправить письмо подтверждения. Ответ JSON."""
    if not _check_subscribe_rate_limit(request):
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Слишком частые запросы. Попробуйте позже."]}},
            status=429,
        )
    form = SubscribeForm(request.POST)
    if not form.is_valid():
        errors = {k: [str(e) for e in v] for k, v in form.errors.items()}
        return JsonResponse({"success": False, "errors": errors}, status=400)
    if form.cleaned_data.get("website"):
        return JsonResponse({
            "success": True,
            "message": "Проверьте почту: мы отправили ссылку для подтверждения подписки.",
        })
    email = form.cleaned_data["email"].lower().strip()
    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
    try:
        with transaction.atomic():
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={
                    "ip_address": ip or None,
                    "user_agent": user_agent,
                },
            )
            if not created:
                subscriber.ip_address = ip or subscriber.ip_address
                subscriber.user_agent = user_agent
                subscriber.save(update_fields=["ip_address", "user_agent"])
            if subscriber.is_active:
                return JsonResponse({
                    "success": True,
                    "message": "Вы уже подписаны на рассылку.",
                })
            confirm_url = request.build_absolute_uri(
                reverse("confirm_subscription", kwargs={"token": str(subscriber.confirmation_token)})
            )
            subject = "Подтвердите подписку на рассылку"
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")
            ctx = {"confirm_url": confirm_url}
            html_message = render_to_string("emails/subscribe_confirm.html", ctx)
            text_message = render_to_string("emails/subscribe_confirm.txt", ctx)
            send_mail(
                subject=subject,
                message=text_message,
                from_email=from_email,
                recipient_list=[email],
                fail_silently=False,
                html_message=html_message,
            )
        return JsonResponse({
            "success": True,
            "message": "Проверьте почту: мы отправили ссылку для подтверждения подписки.",
        })
    except Exception as e:
        logger.exception("Subscribe error for %s: %s", email, e)
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Произошла ошибка. Попробуйте позже."]}},
            status=500,
        )


@require_http_methods(["GET"])
def confirm_subscription_view(request, token):
    """Подтверждение подписки по токену из письма."""
    subscriber = get_object_or_404(Subscriber, confirmation_token=token)
    if subscriber.is_active:
        messages.success(request, "Ваша подписка уже была подтверждена ранее.")
    else:
        subscriber.is_active = True
        subscriber.confirmed_at = timezone.now()
        subscriber.save(update_fields=["is_active", "confirmed_at"])
        messages.success(request, "Подписка успешно подтверждена. Спасибо!")
    return render(request, "subscribe_confirm.html", {"subscriber": subscriber})


def _check_application_rate_limit(request):
    """Один запрос заявки в APPLICATION_RATE_LIMIT_SECONDS по сессии."""
    key = "application_last_attempt"
    now = time.time()
    last = request.session.get(key)
    if last is not None and (now - last) < APPLICATION_RATE_LIMIT_SECONDS:
        return False
    request.session[key] = now
    return True


@require_http_methods(["POST"])
def application_submit_view(request):
    """POST: принять заявку, сохранить в БД, отправить письмо-подтверждение. Ответ JSON."""
    if not _check_application_rate_limit(request):
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Слишком частые запросы. Попробуйте позже."]}},
            status=429,
        )
    form = ApplicationForm(request.POST)
    if not form.is_valid():
        errors = {k: [str(e) for e in v] for k, v in form.errors.items()}
        return JsonResponse({"success": False, "errors": errors}, status=400)
    try:
        with transaction.atomic():
            application = form.save()
        email = application.email
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")
        subject = "Ваша заявка принята"
        ctx = {"name": application.name, "message_text": application.message or "—"}
        html_message = render_to_string("emails/application_confirm.html", ctx)
        text_message = render_to_string("emails/application_confirm.txt", ctx)
        send_mail(
            subject=subject,
            message=text_message,
            from_email=from_email,
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message,
        )
        return JsonResponse({
            "success": True,
            "message": "Заявка отправлена. Мы свяжемся с вами в ближайшее время.",
        })
    except Exception as e:
        logger.exception("Application submit error: %s", e)
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Произошла ошибка. Попробуйте позже."]}},
            status=500,
        )
