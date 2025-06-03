from django.urls import path
from . import views
from .views import status_view

urlpatterns = [
    path('', views.dashboard, name='rpg_dashboard'),
    path('status/', views.status_view, name='status_view'),
    path('log/', views.log_action, name='log_action'),
]
