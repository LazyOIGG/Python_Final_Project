from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="课程名称")
    teacher = models.CharField(max_length=100, verbose_name="授课教师")
    description = models.TextField(blank=True, verbose_name="课程描述")
    capacity = models.PositiveIntegerField(default=30, verbose_name="课程容量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"{self.name} - {self.teacher}"

    def available_seats(self):
        """返回剩余可选名额"""
        return self.capacity - self.enrollment_set.count()

    def is_full(self):
        """检查课程是否已满"""
        return self.available_seats() <= 0


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="选课时间")

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "选课记录"
        verbose_name_plural = "选课记录"

    def __str__(self):
        return f"{self.student.username} 选修了 {self.course.name}"