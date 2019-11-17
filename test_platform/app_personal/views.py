from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # return render(request, 'manage.html')
            auth.login(request, user) #记录用户的登录状态
            return redirect('/manage/')
        elif username == '' or password == '':
            error = 'username or password is not null'
            return render(request, 'login.html', {
                'error':error
            })
        else:
            error = 'username or password is error!'
            return render(request,'login.html',{
                'error':error
            })


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/login/')


