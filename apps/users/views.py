import os
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operations.models import UserProfile, UserCourse, UserFavorite, UserMessage
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from apps.users.forms import LoginForm, DynamicLoginForm, RegisterGetForm, RegisterPostForm, UploadImageForm, \
    UserInfoForm, ChangePwdForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# def message_nums(request):
#     if request.user.is_authenticated:
#         return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
#     else:
#         return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = 'mymessage'
        messages = UserMessage.objects.filter(user=request.user)
        for message in messages:
            message.has_read=True
            message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=10, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        my_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        orgs = []
        for fav_org in my_fav_orgs:
            try:
                org = CourseOrg.objects.get(id=fav_org.fav_id)
                orgs.append(org)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-org.html", {
            "current_page": current_page,
            "orgs": orgs,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        my_fav_course = UserFavorite.objects.filter(user=request.user, fav_type=1)
        courses = []
        for fav_course in my_fav_course:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                courses.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html", {
            "current_page": current_page,
            "courses": courses,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        my_fav_teacher = UserFavorite.objects.filter(fav_type=3)
        teachers = []
        for fav_teacher in my_fav_teacher:
            try:
                teacher = Teacher.objects.get(id=fav_teacher.fav_id)
                teachers.append(teacher)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-teacher.html", {
            "current_page": current_page,
            "teachers": teachers,
        })


class MyCourseView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        user_courses = UserCourse.objects.filter(user=request.user)
        courses = [user_course.course for user_course in user_courses]
        return render(request, "usercenter-mycourse.html", {
            "courses": courses,
            "current_page": current_page,
        })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = pwd_form.cleaned_data['password1']
            user = request.user
            user.set_password(pwd1)
            user.save()
            login(request, user)
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    # def save_file(self, file):
    #     BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #     path = os.path.join(BASE_DIR, 'media', 'head_image', 'uploaded.jpg')
    #     with open(path, "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)  # instance指明修改的实例
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "current_page": current_page,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(user_info_form.errors)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        return render(request, "login.html", {
            "next": next,
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)  # 创建表单用于验证数据
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            # 表单验证
            if not user_name:
                return render(request, "login.html", {"msg": "请输入用户名"})
            if not password:
                return render(request, "login.html", {"msg": "请输入密码"})
            # 用户查询（通过用户名和加密后的密码）
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))  # 重定向url，调用reverse函数通过urlname来反向解析url
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form,
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            email = register_post_form.cleaned_data["email"]
            password = register_post_form.cleaned_data["password"]
            user = UserProfile(username=email, email=email)
            user.set_password(password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form,
            })
