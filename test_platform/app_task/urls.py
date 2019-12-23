from django.urls import path, include
from . import views

urlpatterns = [
    # 任务管理
    path('task_list/', views.task_list),
    path('task_add/', views.task_add),
    path('case_node/',views.case_node),
    path('save_task/', views.save_task),
    path('task_edit/<int:tid>/', views.task_edit),
    path('task_run/<int:tid>/', views.task_rung),
    path('task_log/<int:tid>/', views.task_log),
    path('get_log/', views.get_log),
    ]


