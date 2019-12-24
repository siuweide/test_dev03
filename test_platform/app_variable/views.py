from django.shortcuts import render
from django.http import JsonResponse
from app_variable.models import variable

# Create your views here.

def variable_list(request):
    """ 变量列表 """
    v = variable.objects.all()
    return render(request, "variable/list.html",{
        "variable":v
    })

def variable_save(request):
    """ 保存变量 """
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        key = request.POST.get("req_key", "")
        value = request.POST.get("req_value", "")
        desc = request.POST.get("req_desc", "")
        print("vid============>", type(vid),vid)

        if key == "" or value == "":
            return JsonResponse({"status":10102, "message":"key or value is not null"})

        if vid == "0":
            variable.objects.create(key=key,
                                    value=value,
                                    describe=desc)
        else:
            var = variable.objects.get(id=vid)
            var.key = key
            var.value = value
            var.desc = desc
            var.save()
        return JsonResponse({"status":10200, "message":"创建变量成功"})
    else:
        return JsonResponse({"status":10101, "message":"请求失败"})

def variable_delete(request):
    """ 删除变量 """
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        variable.objects.get(id=vid).delete()
        return JsonResponse({"status":10200, "message":"删除变量成功"})
    else:
        return JsonResponse({"status":10101, "message":"请求失败"})