# 学生选课信息管理系统 - Django项目

![Django](https://img.shields.io/badge/Django-3.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-blue.svg)

一个基于Django框架开发的学生选课系统，提供课程浏览、选课退课、用户注册登录等功能。

## 功能特性

- **用户认证系统**
  - 注册/登录/退出功能
  - 基于Django内置用户模型
  - 登录保护所有功能页面

- **课程管理**
  - 查看所有课程列表
  - 课程详细信息展示
  - 课程容量限制
  - 选课人数统计

- **选课功能**
  - 学生选课/退课操作
  - 防止重复选课
  - 我的课程查看
  - 选课状态标识

- **数据可视化**
  - 课程选课热度图表
  - 使用Chart.js实现
  - 显示选课比例

## 技术栈

- **后端框架**: Django 5.2
- **前端框架**: Bootstrap 5
- **数据库**: SQLite (开发环境)
- **数据可视化**: Chart.js
- **部署**: ASGI/WSGI

## 项目结构

```
Python_Final_Project/
├── courses/                          # 主应用
│   ├── migrations/                   # 数据库迁移文件
│   ├── templates/courses/            # 模板文件
│   │   ├── course_list.html          # 课程列表页
│   │   ├── index.html                # 首页
│   │   ├── login.html                # 登录页
│   │   ├── my_courses.html           # 我的课程页
│   │   └── register.html             # 注册页
│   ├── admin.py                      # 管理后台配置
│   ├── apps.py                       # 应用配置
│   ├── models.py                     # 数据模型
│   ├── tests.py                      # 测试文件
│   ├── urls.py                       # 应用路由
│   └── views.py                      # 视图函数
├── Python_Final_Project/             # 项目配置
│   ├── settings.py                   # 项目设置
│   ├── urls.py                       # 主路由
│   ├── asgi.py                       # ASGI配置
│   └── wsgi.py                       # WSGI配置
├── db.sqlite3                        # 数据库文件
└── manage.py                         # 管理脚本
```

## 安装与运行

1. **克隆仓库**
   ```bash
   git clone [仓库地址]
   cd Python_Final_Project
   ```

2. **安装依赖**
   ```bash
   pip install django
   ```

3. **数据库迁移**
   ```bash
   python manage.py migrate
   ```

4. **创建超级用户(可选)**
   ```bash
   python manage.py createsuperuser
   ```

5. **运行开发服务器**
   ```bash
   python manage.py runserver
   ```

6. **访问应用**
   - 打开浏览器访问: http://127.0.0.1:8000
   - 管理员后台: http://127.0.0.1:8000/admin

## 使用说明

1. **注册账号**
   - 访问/register页面创建新账户

2. **登录系统**
   - 使用注册的凭证登录

3. **浏览课程**
   - 查看所有可用课程
   - 图表显示选课热度

4. **选课操作**
   - 点击"选课"按钮选择课程
   - 已选课程显示"已选"标记

5. **管理课程**
   - 在"我的课程"页面可退课
   - 查看当前已选课程列表

## 许可证

MIT License