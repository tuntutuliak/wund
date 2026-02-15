
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('teachers/', views.team, name='team'),
    path('programs/', views.programms, name='programms'),
    path('svedeniya/', RedirectView.as_view(url='/contacts/', permanent=True)),
]
