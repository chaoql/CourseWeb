from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male", "男"),
    ("famale", "女"),
)


class BaseModel(models.Model):
    """
    用于存放多个模型共用的数据列，且不生成该类的数据表
    """
    add_time = models.DateTimeField(default=datetime.now, verbose_name="数据添加时间")

    class Meta:
        # 防止父类建表
        abstract = True


class UserProfile(AbstractUser):
    """
    重写用户模型类，继承自 AbstractUser
    """
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    # mobile = models.CharField(max_length=11, unique=True, verbose_name="电话号码")
    mobile = models.CharField(max_length=11, verbose_name="电话号码")
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y%m", default="default.jpg")

    class Meta:
        """
        对当前表进行相关设置
        """
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_nums(self):
        return self.usermessage_set.filter(has_read=False).count()

    def __str__(self):
        """返回一个对象的描述信息"""
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
