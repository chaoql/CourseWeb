from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.operations.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, RegisterGetForm, RegisterPostForm


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
