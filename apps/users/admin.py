from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


# admin.site.register(UserProfile, UserAdmin)  # 在后台管理系统中注入该数据表
