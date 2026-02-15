from django.shortcuts import render


def home(request):
    """Главная страница — рендер base.html с контентом по умолчанию."""
    return render(request, 'base.html')


def testimonials(request):
    """Страница отзывов — та же функциональность, что и school-site/templates/testimonials.html."""
    return render(request, 'testimonials.html')


def about(request):
    """Страница «О нас»."""
    return render(request, 'about.html')


def contacts(request):
    """Контакты и сведения об образовательной организации."""
    return render(request, 'contacts.html')


def team(request):
    """Страница «Преподаватели»."""
    return render(request, 'team.html')
