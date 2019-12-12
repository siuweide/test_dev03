from django.urls import path, include
from . import views

urlpatterns = [
    # 任务管理
    path('task_list/', views.task_list),
    path('task_add/', views.task_add)
    ]


