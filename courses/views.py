from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# 课程列表视图
@login_required  # 要求用户登录后才能访问
def course_list(request):
    """
    显示所有课程列表及当前用户选课状态
    功能：
    1. 获取所有课程及每门课程的选课人数统计
    2. 获取当前用户已选课程ID列表
    3. 渲染课程列表模板
    """
    courses = Course.objects.all().annotate(enrollment_count=Count('enrollment'))
    enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
    })


# 选课视图
@login_required
def enroll_course(request, course_id):
    """
    处理选课请求
    参数：
    - course_id: 要选的课程ID
    逻辑：
    1. 检查课程是否存在(404处理)
    2. 创建选课记录(如不存在)
    3. 重定向到"我的课程"页面
    """
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('my_courses')


# 我的课程视图
@login_required
def my_courses(request):
    """
    显示当前用户已选课程列表
    返回：
    - 渲染包含用户选课记录的模板
    """
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})


# 退课视图
@login_required
def drop_course(request, course_id):
    """
    处理退课请求
    参数：
    - course_id: 要退的课程ID
    逻辑：
    1. 删除当前用户对该课程的选课记录
    2. 重定向到"我的课程"页面
    """
    Enrollment.objects.filter(student=request.user, course_id=course_id).delete()
    return redirect('my_courses')


# 用户注册视图
def register_view(request):
    """
    处理用户注册
    支持方法：
    - GET: 显示注册表单
    - POST: 处理注册请求
    逻辑：
    1. 检查用户名是否已存在
    2. 创建新用户或返回错误
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        else:
            return HttpResponse("用户已存在！")
    return render(request, "courses/register.html")


# 用户登录视图
def login_view(request):
    """
    处理用户登录
    支持方法：
    - GET: 显示登录表单
    - POST: 处理登录请求
    逻辑：
    1. 验证用户凭证
    2. 登录成功则建立会话，失败返回错误
    """
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


# 用户退出视图
def logout_view(request):
    """
    处理用户退出
    逻辑：
    1. 清除用户会话
    2. 重定向到登录页面
    """
    logout(request)
    return redirect("login")


# 首页视图
@login_required
def index(request):
    """
    登录后首页
    功能：
    - 显示用户欢迎信息和主要功能入口
    """
    return render(request, "courses/index.html")
