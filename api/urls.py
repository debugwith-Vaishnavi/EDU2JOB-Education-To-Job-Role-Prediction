# api/urls.py
from django.urls import path
from .views import register_view, login_view, profile_view, predict_view, history_view


urlpatterns = [
    path('result/', lambda request: render(request, 'result.html')),
path('profile/', lambda request: render(request, 'profile.html')),
path('history/', lambda request: render(request, 'history.html')),
path('predict/', lambda request: render(request, 'predict.html')),
path('dashboard/', lambda request: render(request, 'dashboard.html')),
path('register/', lambda request: render(request, 'register.html')),
]
