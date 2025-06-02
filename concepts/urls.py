from django.urls import path
from .views import create_concept, list_concepts
from . import views

urlpatterns = [
    path('', views.list_concepts, name='list_concepts'),
    path('create/', views.create_concept, name='create_concept'),
    path('<int:concept_id>/', views.detail_concept, name='detail_concept'),
    path('<int:concept_id>/edit/', views.edit_concept, name='edit_concept'),  # 編集
    path('<int:concept_id>/delete/', views.delete_concept, name='delete_concept'),  # 削除
]
