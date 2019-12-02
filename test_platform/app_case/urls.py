from django.urls import path, include
from . import views

urlpatterns = [
    # 用例管理
    path('', views.add_case),
    path('send_req/', views.send_req),
    path('assert_result/', views.assert_result),
    path('get_select_data/', views.get_select_data),
    path('save_case/',views.save_case),
    path('list_case/', views.list_case),
    ]
