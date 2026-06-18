from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    return render(request, "dashboard.html")


def profile_page(request):
    return render(request, "profile.html")


def history_page(request):
    return render(request, "history.html")


def predict_page(request):
    return render(request, "predict.html")


def result_page(request):
    return render(request, "result.html")


urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('profile/', profile_page, name='profile'),
    path('predict/', predict_page, name='predict'),
    path('history/', history_page, name='history'),
    path('result/', result_page, name='result'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]