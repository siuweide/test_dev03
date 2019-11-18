from django.urls import path, include
from app_manage import views

urlpatterns = [
    path('', views.manage),
    path('add/', views.project_add),
    path('edit/<int:pid>/', views.project_edit),
    ]