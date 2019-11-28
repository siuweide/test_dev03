from django.urls import path, include
from . import views

urlpatterns = [
    # 用例管理
    path('', views.list_case),
    path('send_req/', views.send_req),
    path('assert_result/', views.assert_result),
    ]
