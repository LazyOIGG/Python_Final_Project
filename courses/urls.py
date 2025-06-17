from django.urls import path  # 导入Django的路由配置函数
from . import views  # 从当前目录导入views模块

# URL模式列表，Django会按顺序匹配请求的URL
urlpatterns = [
    # 首页路由
    # 路径: 根路径('/')
    # 对应视图: views.index
    # 名称: 'index'（在模板中可用{% url 'index' %}引用）
    path('', views.index, name='index'),  # 登录后首页

    # 用户认证相关路由
    path('register/', views.register_view, name='register'),  # 用户注册
    path('login/', views.login_view, name='login'),  # 用户登录
    path('logout/', views.logout_view, name='logout'),  # 用户退出

    # 课程功能相关路由
    path('courses/', views.course_list, name='course_list'),  # 课程列表页

    # 带参数的路由：<int:course_id>表示捕获整数类型的course_id参数
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),  # 选课

    path('my-courses/', views.my_courses, name='my_courses'),  # 我的课程页

    # 带参数的路由
    path('drop/<int:course_id>/', views.drop_course, name='drop_course'),  # 退课
]