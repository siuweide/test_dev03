from django.shortcuts import render

def task_list(request):
    """ 任务列表 """
    return render(request, 'task/list.html')

def task_add(request):
    """ 创建任务 """
    return render(request, 'task/add.html')
