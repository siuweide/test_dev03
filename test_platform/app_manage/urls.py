from django.urls import path, include
from app_manage.views import project_view, module_view

urlpatterns = [
    # 项目管理
    path('', project_view.list_project),
    path('project_list/', project_view.list_project),
    path('project_add/', project_view.project_add),
    path('project_edit/<int:pid>/', project_view.project_edit),
    path('project_delete/<int:pid>/', project_view.project_delete),

    # 模块管理
    path('module_list/', module_view.list_module),
    path('module_add/', module_view.module_add),
    path('module_edit/<int:mid>/', module_view.module_edit),
    path('module_delete/<int:mid>/', module_view.module_delete),
    ]