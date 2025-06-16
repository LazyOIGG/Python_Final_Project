from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 登录后首页
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 新增课程功能
    path('courses/', views.course_list, name='course_list'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('drop/<int:course_id>/', views.drop_course, name='drop_course'),
]