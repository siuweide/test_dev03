import re
import json
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.forms.models import model_to_dict
from app_manage.models import Project,Module
from app_case.models import TestCase
from app_variable.models import variable


def list_case(request):
    ''' 用例列表 '''
    case_projects = TestCase.objects.all()
    p = Paginator(case_projects, 2)
    page = request.GET.get('page')
    print('page-------------------->',page)
    if page == '':
        page = 1
    try:
        case_projects = p.page(page)
    except PageNotAnInteger:
        case_projects = p.page(1)
    except EmptyPage:
        case_projects = p.page(p.num_pages)
    return render(request,'case/list.html',{
        'case_projects':case_projects
    })

def add_case(request):
    ''' 添加用例 '''
    return render(request, 'case/add.html')

def edit_case(request,cid):
    ''' 编辑用例 '''
    return render(request, 'case/edit.html')

def send_req(request):
    """
    发送接口
    """
    if request.method == "GET":
        url = request.GET.get("url", "")
        method = request.GET.get("method", "")
        header = request.GET.get("header", "")
        per_type = request.GET.get("per_type", "")
        per_value = request.GET.get("per_value", "")

        if url == "":
            return JsonResponse({"code": 10101, "message": "URL不能为空！"})
        elif "${" in url and "}" in url:
            key = re.findall(r"\${(.+?)}", url)
            url = variable.objects.get(key=key[0]).value
            print("variable========>",url)

        try:
            header = json.loads(header)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10102, "message": "Header格式错误，必须是标准的JSON格式！"})

        try:
            per_value = json.loads(per_value)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"code": 10103,
             "message": "参数格式错误，必须是标准的JSON格式！"})

        if method == "get":
            r = requests.get(url, params=per_value, headers=header)

        if method == "post":
            print("post")
            if per_type == "form":
                r = requests.post(url, data=per_value, headers=header)

            if per_type == "json":
                r = requests.post(url, json=per_value, headers=header)


        return JsonResponse({"code": 10200, "message":"success", "data": r.text})

def assert_result(request):
    """ 断言结果 """
    if request.method == "POST":
        result_text = request.POST.get("result_text", "")
        assert_text = request.POST.get("assert_text", "")
        assert_type = request.POST.get("assert_type", "")

        if result_text == "" or assert_text == "":
            return JsonResponse({"code": 10101, "message":"断言的参数不能为空"})

        if assert_type != "include" and assert_type != "equal":
            return JsonResponse({"code": 10102, "message":"断言的参数不能为空"})

        if assert_type == "include":
            if assert_text in result_text:
                return JsonResponse({"code": 10200, "message":"断言包含成功"})
            else:
                return JsonResponse({"code": 10103, "message":"断言包含失败"})

        if assert_type == "equal":
            if assert_text == result_text:
                return JsonResponse({"code": 10104, "message":"断言相等"})
            else:
                return JsonResponse({"code": 10105, "message":"断言失败"})

        return JsonResponse({"code": 10106, "message":"fail"})


def get_select_data(request):
    """获取项目/模块的数据"""
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for p in projects:
            project_dict = {
                "id":p.id,
                "name":p.name
            }
            modules = Module.objects.filter(project_id=p.id)
            module_list = []
            for m in modules:
                module_dict = {
                    "id":m.id,
                    "name":m.name
                }
                module_list.append(module_dict)
            project_dict["moduleList"] = module_list

            data_list.append(project_dict)
        return JsonResponse({"code":10200, "message":"success", "data":data_list})

def save_case(request):
    """ 保存用例 """
    if request.method == "POST":
        case_id = request.POST.get("cid","")
        url = request.POST.get("url","")
        method = request.POST.get("method","")
        header = request.POST.get("header","")
        per_type = request.POST.get("per_type","")
        per_value = request.POST.get("per_value","")
        result_text = request.POST.get("result_text","")
        assert_text = request.POST.get("assert_text","")
        assert_type = request.POST.get("assert_type","")
        module_id = request.POST.get("module_id","")
        case_name = request.POST.get("case_name","")

        print('-------------case_id----------',case_id)

        if method == "get":
            method_int = 1
        elif method == "post":
            method_int = 2
        else:
            return JsonResponse({"code":10101,"message":"请求方法错误"})

        if per_type == "form":
            per_type_int = 1
        elif per_type == "json":
            per_type_int = 2
        else:
            return JsonResponse({"code":10102,"message":"参数类型错误"})

        if assert_type == "include":
            assert_type_int = 1
        elif assert_type == "equal":
            assert_type_int = 2
        else:
            return JsonResponse({"code":10103,"message":"断言类型类型错误"})

        if case_id == "":
            print('-----------create--------------')
            TestCase.objects.create(module_id=module_id,
                                    name=case_name,
                                    url=url,
                                    method=method_int,
                                    header=header,
                                    parameter_type=per_type_int,
                                    parameter_body=per_value,
                                    result=result_text,
                                    assert_type=assert_type_int,
                                    assert_text=assert_text)
            return JsonResponse({"code":10200,"message":"create success"})
        else:
            print('-----------save--------------')
            case = TestCase.objects.get(id=case_id)
            case.url = url
            case.method = method_int
            case.header = header
            case.per_type = per_type_int
            case.per_value = per_value
            case.result_text = result_text
            case.assert_text = assert_text
            case.assert_type = assert_type_int
            case.module_id = module_id
            case.name = case_name
            case.save()
            return JsonResponse({"code":10200,"message":"save success"})
    else:
        return JsonResponse({"code":10100,"message":"请求方法错误"})

def get_case_info(request):
    """ 获取用例信息 """
    if request.method == "POST":
        cid = request.POST.get('cid','')
        case = TestCase.objects.get(id=cid)
        module = Module.objects.get(id=case.module_id)
        case_info = model_to_dict(case)
        case_info['project'] = module.project_id

        return JsonResponse({"code":10200, "message": "save success","data":case_info})
    else:
        return JsonResponse({"code":10100, "message": "请求方法错误"})

def delete_case(request):
    """ 删除用例 """
    if request.method == "POST":
        cid = request.POST.get('cid','')
        case = TestCase.objects.get(id=cid)
        case.delete()
        return JsonResponse({"code":10200, "message": "delete success"})
    else:
        return JsonResponse({"code":10100, "message": "请求方法错误"})