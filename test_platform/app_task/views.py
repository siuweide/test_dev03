import json
import os
from xml.dom.minidom import parse
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app_case.models import TestCase
from app_manage.models import Project,Module
from app_task.models import TestTask,TestResult
from app_task.setting import TASK_DATA,TASK_RUN,TASK_RESULTS
from app_task.extend.task_thread import TaskThread

def task_list(request):
    """ 任务列表 """
    task = TestTask.objects.all()
    return render(request, 'task/list.html',{
        "task":task
    })

def task_add(request):
    """ 创建任务 """
    return render(request, 'task/add.html')

def case_node(request):
    """用例的树形节点"""
    if request.method == "GET":
        data = []
        project = Project.objects.all()


        for p in project:
            project_dict = {
                "name": p.name,
                "isParent": True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name": m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    case_dict = {
                        "id": c.id,
                        "name": c.name,
                        "isParent": False,
                    }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data.append(project_dict)
        return JsonResponse({"code": 10200, "message": "success","data":data})

    elif request.method == "POST":
        task_id = request.POST.get("tid", "")
        task = TestTask.objects.get(id=task_id)
        case_list = task.cases[1:-1].split(",")
        case_list_int = []
        for c in case_list:
            case_list_int.append(int(c))

        task_data = {
            "taskName":task.name,
            "taskDesc":task.describe
        }

        data = []
        project = Project.objects.all()
        for p in project:
            project_dict = {
                "name": p.name,
                "isParent": True
            }
            module = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in module:
                module_dict = {
                    "name": m.name,
                    "isParent": True
                }
                case = TestCase.objects.filter(module_id=m.id)
                case_list = []
                for c in case:
                    if c.id in case_list_int:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": True
                        }
                    else:
                        case_dict = {
                            "id": c.id,
                            "name": c.name,
                            "isParent": False,
                            "checked": False
                        }
                    case_list.append(case_dict)
                module_dict["children"] = case_list
                module_list.append(module_dict)
            project_dict["children"] = module_list
            data.append(project_dict)
        task_data['data'] = data
        return JsonResponse({"code": 10200, "message": "success","data":task_data})


def save_task(request):
    """保存任务"""
    if request.method == "POST":
        task_id = request.POST.get("tid", "")
        print('task_id---------->',type(task_id),task_id)
        task_name = request.POST.get("name", "")
        print('task_name------------------->',task_name)
        task_desc = request.POST.get("desc", "")
        print('task_desc------------------->',task_desc)
        task_cases = request.POST.get("cases", "")
        print('task_cases------------------->',task_cases)
        if task_name == "":
            return JsonResponse({"status":10102, "message":"任务的名称为空"})

        if task_id == "0":
            print("task_id-------------->",task_id)
            print('11111111111111')
            try:
                TestTask.objects.create(name=task_name,
                                        describe=task_desc,
                                        cases=task_cases)
            except:
                print("执行失败啊")
        else:
            print("task_id-------------->",task_id)
            task = TestTask.objects.get(id=task_id)
            task.name = task_name
            task.describe = task_desc
            task.cases = task_cases
            task.save()
        return JsonResponse({"status":10200, "message":"成功"})
    else:
        return JsonResponse({"status":10101, "message":"请求方法错误"})


def task_edit(request, tid):
    """ 编辑任务 """
    return render(request, "task/edit.html")


def task_rung(request, tid):
    """ 运行任务 """
    task = TaskThread(tid)
    task.run()
    return redirect("/task/task_list/")

def task_log(request,tid):
    """ 日志管理 """
    print('tid----------->',tid)
    results = TestResult.objects.filter(task_id=tid)
    return render(request, "task/log.html" ,{
        "results":results
    })

def get_log(request):
    """ 获取日志 """
    if request.method == "POST":
        rid = request.POST.get("rid", "")
        result = TestResult.objects.get(id=rid)
        return JsonResponse({"status":10200, "message":"获取日志成功","data":result.result})