from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app_manage.models import Project, Module
from app_manage.form import ProjectForm,ProjectEditFrom


def list_module(request):
    """
    模块管理
    """
    module_list = Module.objects.all()
    return render(request, 'module/list.html', {
        'modules':module_list
    })