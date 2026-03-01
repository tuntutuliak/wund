from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import News, Teacher, ContactSection

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
    """Страница «Программы» (MOCK: список из MOCK_COURSES)."""
    return render(request, 'programms.html', {'courses': MOCK_COURSES})


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
    return render(request, 'group_course.html')
