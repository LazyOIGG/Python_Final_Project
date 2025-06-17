from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Enrollment


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 测试数据初始化
        cls.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.course = Course.objects.create(
            name="Python高级编程",
            teacher="张教授",
            capacity=30
        )

    def test_course_creation(self):
        """测试课程模型创建"""
        self.assertEqual(self.course.name, "Python高级编程")
        self.assertEqual(self.course.available_seats(), 30)
        self.assertFalse(self.course.is_full())

    def test_available_seats_calculation(self):
        """测试剩余座位计算逻辑"""
        # 初始容量
        self.assertEqual(self.course.available_seats(), 30)

        # 模拟选课
        Enrollment.objects.create(
            student=self.test_user,
            course=self.course
        )
        self.assertEqual(self.course.available_seats(), 29)

    def test_is_full_method(self):
        """测试课程是否已满的判断"""
        # 将课程容量设为1进行测试
        self.course.capacity = 1
        self.course.save()

        self.assertFalse(self.course.is_full())
        Enrollment.objects.create(
            student=self.test_user,
            course=self.course
        )
        self.assertTrue(self.course.is_full())

    def test_string_representation(self):
        """测试模型的字符串表示"""
        self.assertEqual(
            str(self.course),
            "Python高级编程 - 张教授"
        )


class EnrollmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='enroll_test',
            password='test123'
        )
        cls.course = Course.objects.create(
            name="数据库系统",
            teacher="李教授"
        )

    def test_enrollment_creation(self):
        """测试选课记录创建"""
        enrollment = Enrollment.objects.create(
            student=self.user,
            course=self.course
        )
        self.assertEqual(enrollment.student.username, 'enroll_test')
        self.assertEqual(enrollment.course.name, "数据库系统")
        self.assertIsNotNone(enrollment.enrolled_at)

    def test_unique_together_constraint(self):
        """测试学生-课程唯一约束"""
        Enrollment.objects.create(
            student=self.user,
            course=self.course
        )
        # 尝试重复选课应该抛出异常
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student=self.user,
                course=self.course
            )


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view_get(self):
        """测试登录页GET请求"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/login.html')
        self.assertContains(response, '用户登录')

    def test_login_view_post_success(self):
        """测试成功登录"""
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'testpass123'},
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_post_failure(self):
        """测试失败登录"""
        response = self.client.post(
            reverse('login'),
            {'username': 'wrong', 'password': 'wrong'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '用户名或密码错误')

    def test_logout_view(self):
        """测试退出登录"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_view_get(self):
        """测试注册页GET请求"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '用户注册')

    def test_register_view_post_success(self):
        """测试成功注册"""
        response = self.client.post(
            reverse('register'),
            {'username': 'newuser', 'password': 'newpass123'},
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_duplicate(self):
        """测试重复用户名注册"""
        User.objects.create_user(username='existing', password='test123')
        response = self.client.post(
            reverse('register'),
            {'username': 'existing', 'password': 'test123'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '用户已存在')


class CourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='coursetest',
            password='testpass'
        )
        cls.course1 = Course.objects.create(
            name="Web开发",
            teacher="王老师",
            capacity=20
        )
        cls.course2 = Course.objects.create(
            name="人工智能",
            teacher="赵教授",
            capacity=15
        )
        Enrollment.objects.create(
            student=cls.user,
            course=cls.course1
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='coursetest', password='testpass')

    def test_course_list_view_authenticated(self):
        """测试认证用户访问课程列表"""
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course_list.html')
        self.assertEqual(len(response.context['courses']), 2)
        self.assertContains(response, 'Web开发')

    def test_course_list_view_unauthenticated(self):
        """测试未认证用户访问课程列表（应重定向）"""
        self.client.logout()
        response = self.client.get(reverse('course_list'), follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('course_list')}"
        )

    def test_enrolled_courses_display(self):
        """测试已选课程标记显示"""
        response = self.client.get(reverse('course_list'))
        # 检查已选课程是否有正确标记
        self.assertContains(response, '✅ 已选')
        # 检查未选课程是否有选课按钮
        self.assertContains(response, '选课')


class EnrollmentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='enrolltest',
            password='testpass'
        )
        cls.course = Course.objects.create(
            name="软件工程",
            teacher="孙教授",
            capacity=1  # 设置为1便于测试满员情况
        )

    def setUp(self):
        self.client = Client()
        self.client.login(username='enrolltest', password='testpass')

    def test_enroll_course_success(self):
        """测试成功选课"""
        response = self.client.get(
            reverse('enroll_course', args=[self.course.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('my_courses'))
        self.assertTrue(
            Enrollment.objects.filter(
                student=self.user,
                course=self.course
            ).exists()
        )
        self.assertContains(response, '软件工程')  # 检查重定向后页面

    def test_enroll_course_duplicate(self):
        """测试重复选课（应静默处理）"""
        # 第一次选课
        self.client.get(reverse('enroll_course', args=[self.course.id]))
        # 第二次选课
        response = self.client.get(
            reverse('enroll_course', args=[self.course.id]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # 检查选课记录只有一条
        self.assertEqual(
            Enrollment.objects.filter(
                student=self.user,
                course=self.course
            ).count(),
            1
        )

    def test_enroll_full_course(self):
        """测试选已满课程"""
        # 先让另一个用户占满课程
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass'
        )
        Enrollment.objects.create(
            student=other_user,
            course=self.course
        )

        response = self.client.get(
            reverse('enroll_course', args=[self.course.id]),
            follow=True
        )
        # 检查是否仍然重定向（虽然课程已满）
        self.assertRedirects(response, reverse('my_courses'))
        # 检查当前用户没有选课成功
        self.assertFalse(
            Enrollment.objects.filter(
                student=self.user,
                course=self.course
            ).exists()
        )


class MyCoursesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1',
            password='test123'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='test123'
        )
        cls.course1 = Course.objects.create(
            name="计算机网络",
            teacher="周老师"
        )
        cls.course2 = Course.objects.create(
            name="操作系统",
            teacher="吴教授"
        )
        # user1选了两门课
        Enrollment.objects.create(student=cls.user1, course=cls.course1)
        Enrollment.objects.create(student=cls.user1, course=cls.course2)
        # user2选了一门课
        Enrollment.objects.create(student=cls.user2, course=cls.course1)

    def setUp(self):
        self.client = Client()
        self.client.login(username='user1', password='test123')

    def test_my_courses_view(self):
        """测试我的课程页面"""
        response = self.client.get(reverse('my_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/my_courses.html')
        # 检查返回的选课记录数量
        self.assertEqual(len(response.context['enrollments']), 2)
        self.assertContains(response, '计算机网络')
        self.assertContains(response, '操作系统')

    def test_drop_course(self):
        """测试退课功能"""
        # 先确认有两门课
        response = self.client.get(reverse('my_courses'))
        self.assertEqual(len(response.context['enrollments']), 2)

        # 退掉第一门课
        response = self.client.get(
            reverse('drop_course', args=[self.course1.id]),
            follow=True
        )
        self.assertRedirects(response, reverse('my_courses'))
        # 检查剩余课程
        self.assertEqual(len(response.context['enrollments']), 1)
        self.assertNotContains(response, '计算机网络')
        self.assertContains(response, '操作系统')

    def test_drop_nonexistent_course(self):
        """测试退不存在的课程（应静默处理）"""
        response = self.client.get(
            reverse('drop_course', args=[999]),  # 不存在的课程ID
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # 检查课程数量不变
        self.assertEqual(len(response.context['enrollments']), 2)


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='indextest',
            password='testpass'
        )

    def test_index_authenticated(self):
        """测试认证用户访问首页"""
        self.client.login(username='indextest', password='testpass')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/index.html')
        self.assertContains(response, '欢迎，indextest')

    def test_index_unauthenticated(self):
        """测试未认证用户访问首页（应重定向）"""
        response = self.client.get(reverse('index'), follow=True)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('index')}"
        )