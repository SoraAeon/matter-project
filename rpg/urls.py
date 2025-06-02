from django.urls import path
from . import views

urlpatterns = [
    # 仮に一覧表示だけ
    path('', views.dashboard, name='rpg_dashboard'),
]
