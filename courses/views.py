from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def course_list(request):
    courses = Course.objects.all().annotate(enrollment_count=Count('enrollment'))
    enrolled_courses = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
    })

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('my_courses')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'courses/my_courses.html', {'enrollments': enrollments})

@login_required
def drop_course(request, course_id):
    Enrollment.objects.filter(student=request.user, course_id=course_id).delete()
    return redirect('my_courses')

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
