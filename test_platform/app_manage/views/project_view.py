from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app_manage.models import Project
from app_manage.form import ProjectForm,ProjectEditFrom


# @login_required
def list_project(request):
    """
    项目管理
    """
    username = request.COOKIES.get('user','')
    print('username------------->',username)
    projects = Project.objects.all()
    return render(request, 'project/list.html', {
        'projects':projects,
        'user':username
    })

def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name, describe=describe, status=status)
        return redirect('/manage/')
    else:
        form = ProjectForm()
    return render(request, 'project/add.html', {
        'form':form
    })

def project_edit(request, pid):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']

            p = Project.objects.get(id=pid)
            p.name = name
            p.describe = describe
            p.status = status
            p.save()
        return redirect('/manage/')

    else:
        if pid:
            project = Project.objects.get(id=pid)
            form = ProjectEditFrom(instance=project)
        else:
            form = ProjectForm()
        return render(request, 'project/edit.html', {
            'form':form,
            'id':pid
        })

def project_delete(request, pid):
    if request.method == 'GET':
        project = Project.objects.get(id=pid)
        project.delete()
        return redirect('/manage/')