# api/urls.py
from django.urls import path
from .views import register_view, login_view, profile_view, predict_view, history_view


urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('profile/', profile_view),
    path('predict/', predict_view),
    path('history/', history_view),
   
]
