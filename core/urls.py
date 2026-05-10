from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), # La ruta raíz será el login
    path('dashboard/', views.dashboard_view, name='dashboard'), # Aquí los mandaremos al entrar
]