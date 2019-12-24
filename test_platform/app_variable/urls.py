from django.urls import path, include
from . import views

urlpatterns = [
    # 任务管理
    path('variable_list/', views.variable_list),
    path("variable_save/", views.variable_save),
    path("variable_delete/", views.variable_delete),
    ]


