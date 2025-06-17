from django.db import models
from django.contrib.auth.models import User  # 使用Django内置用户模型


class Course(models.Model):
    """
    课程模型
    对应数据库中的课程表，存储课程基本信息
    """
    # 课程名称字段，CharField类型，最大长度100，在管理后台显示为"课程名称"
    name = models.CharField(max_length=100, verbose_name="课程名称")

    # 授课教师字段，CharField类型，最大长度100
    teacher = models.CharField(max_length=100, verbose_name="授课教师")

    # 课程描述字段，TextField类型，允许为空
    description = models.TextField(blank=True, verbose_name="课程描述")

    # 课程容量字段，正整数类型，默认30人
    capacity = models.PositiveIntegerField(default=30, verbose_name="课程容量")

    # 创建时间字段，自动记录创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        """定义对象的字符串表示形式，用于管理后台和shell显示"""
        return f"{self.name} - {self.teacher}"

    def available_seats(self):
        """
        计算课程剩余可选名额
        方法逻辑：
        1. 通过反向查询(enrollment_set)获取当前课程的选课记录数
        2. 用总容量减去已选人数得到剩余名额
        """
        return self.capacity - self.enrollment_set.count()

    def is_full(self):
        """
        检查课程是否已满
        返回布尔值：
        - True: 已无剩余名额
        - False: 仍有剩余名额
        """
        return self.available_seats() <= 0


class Enrollment(models.Model):
    """
    选课记录模型
    建立学生与课程之间的多对多关系
    """
    # 学生字段，外键关联User模型，级联删除
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="学生"
    )

    # 课程字段，外键关联Course模型，级联删除
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="课程"
    )

    # 选课时间字段，自动记录创建时间
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="选课时间"
    )

    class Meta:
        """
        模型元数据配置
        """
        # 设置学生和课程的联合唯一约束，防止重复选课
        unique_together = ('student', 'course')

        # 配置在管理后台的显示名称
        verbose_name = "选课记录"
        verbose_name_plural = "选课记录"  # 复数形式

    def __str__(self):
        """定义选课记录的字符串表示形式"""
        return f"{self.student.username} 选修了 {self.course.name}"