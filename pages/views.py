from django.shortcuts import render


def home(request):
    """Главная страница — рендер base.html с контентом по умолчанию."""
    return render(request, 'base.html')


def testimonials(request):
    """Страница отзывов — та же функциональность, что и school-site/templates/testimonials.html."""
    return render(request, 'testimonials.html')
