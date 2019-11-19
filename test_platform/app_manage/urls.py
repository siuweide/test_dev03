from django.urls import path, include
from app_manage.views import project_view, module_view

urlpatterns = [
    # 项目管理
    path('', project_view.list_project),
    path('project_add/', project_view.project_add),
    path('project_edit/<int:pid>/', project_view.project_edit),
    path('project_delete/<int:pid>/', project_view.project_delete),

    # 模块管理
    path('2/', module_view.list_module),
    ]