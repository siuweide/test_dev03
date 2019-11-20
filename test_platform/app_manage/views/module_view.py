from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app_manage.models import Project, Module
from app_manage.form import ProjectForm,ProjectEditFrom,ModuleForm


def list_module(request):
    """
    模块管理
    """
    module_list = Module.objects.all()
    return render(request, 'module/list.html', {
        'modules':module_list
    })

def module_add(request):
    ''' 创建模块 '''
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(project=project, name=name, describe=describe)
        return redirect('/manage/module_list/')
    else:
        form = ModuleForm()
        return render(request,'module/add.html',{
            'form':form
        })

def module_edit(request, mid):
    ''' 编辑模块 '''
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']

            m = Module.objects.get(id=mid)
            m.project = project
            m.name = name
            m.describe = describe
            m.save()
        return redirect('/manage/module_list/')
    else:
        if mid:
            m = Module.objects.get(id=mid)
            form = ModuleForm(instance=m)
        else:
            form = ModuleForm()
        return render(request, 'module/edit.html', {
            'form':form,
            'id':mid
        })

def module_delete(request, mid):
    ''' 删除模块 '''
    if request.method == 'GET':
        m = Module.objects.get(id=mid)
        m.delete()
        return redirect('/manage/module_list/')
