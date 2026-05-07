from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
# crée AuthenticationForm
# crée variable form
# l’envoie au template login.html
# Cette ligne importe les pages de login/logout déjà faites par Django

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home_page_rescuetrack"),
    path("caserne/", include("caserne.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # Quand quelqu’un va sur /login/, utilise la vue LoginView de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
