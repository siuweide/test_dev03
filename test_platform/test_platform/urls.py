"""test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_personal import views as personal_view
from app_manage import views as manage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', personal_view.login),
    path('logout/', personal_view.logout),

    # 项目/模块管理
    path('manage/', include('app_manage.urls')),

    # # 模块管理
    # path('module/', include('app_manage.urls')),

]
