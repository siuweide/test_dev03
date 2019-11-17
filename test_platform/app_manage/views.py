from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_manage.models import Project



# @login_required
def manage(request):
    """
    项目管理
    """
    projects = Project.objects.all()
    return render(request, 'project/list.html', {
        'projects':projects
    })

def project_add(request):
    return render(request, 'project/add.html')