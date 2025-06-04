from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        else:
            return HttpResponse("用户已存在！")
    return render(request, "courses/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("用户名或密码错误！")
    return render(request, "courses/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def index(request):
    return render(request, "courses/index.html")
