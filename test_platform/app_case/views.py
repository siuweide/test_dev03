from django.shortcuts import render
from django.http import JsonResponse
import requests
import json



def list_case(request):
    return render(request, 'case/debug.html')


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

        print("url--->", url, type(url))
        print("header--->", header, type(header))
        print("method--->", method, type(method))
        print("per_type--->", per_type, type(per_type))
        print("per_value--->", per_value, type(per_value))
        if url == "":
            return JsonResponse({"code": 10101, "message": "URL不能为空！"})

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