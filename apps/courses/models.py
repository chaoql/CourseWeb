from django.db import models

from apps.organizations.models import Teacher, CourseOrg
from apps.users.models import BaseModel


class Course(BaseModel):
    """
    课程类模型
    """
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    notice = models.CharField(max_length=300, verbose_name="课程公告", default="")
    # is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True, on_delete=models.CASCADE)
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")),
                              max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    # detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/",
    #                       filePath="courses/ueditor/", default='')
    detail = models.TextField(verbose_name="课程详情")
    is_classics = models.BooleanField(default=False, verbose_name="是否经典")

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def Lesson_nums(self):
        return self.lesson_set.all().count()


class CourseTag(BaseModel):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签名")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    """
    课程章节类模型
    """
    # on_delete参数表示对应的外键被删除后，当前数据应该怎么办？CASCADE表示级联删除，SET_NULL表示设置为空
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    """
    课程视频类模型
    """
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, default="", verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    """
    课程资源类模型
    """
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="资源名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
