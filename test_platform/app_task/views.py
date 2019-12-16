from django.http import JsonResponse
from django.shortcuts import render
from app_case.models import TestCase
from app_manage.models import Project,Module
from app_task.models import TestTask

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
        task_id = request.POST.get('tid')
        task = TestTask.objects.get(id=task_id)
        cases_list = task.cases[1:-1].split(",")

        print('task', type(cases_list), cases_list)

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
                    if str(c.id) in cases_list:
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
    """ 保存任务 """

    if request.method == "POST":
        task_name = request.POST.get("name", '')
        task_desc = request.POST.get("desc", '')
        task_cases = request.POST.get("case", '')
        if task_name == '':
            return JsonResponse({"status":10102, "message":"任务的名称为空"})
        TestTask.objects.create(name=task_name,describe=task_desc,cases=task_cases)
        return JsonResponse({"status":10200, "message":"成功"})
    else:
        return JsonResponse({"status":10101, "message":"请求方法错误"})



def task_edit(request, tid):
    """ 编辑任务 """
    return render(request, "task/edit.html")
