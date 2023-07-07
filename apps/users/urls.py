from django.urls import path
from django.views.generic import TemplateView
from apps.users.views import LoginView, LogoutView, RegisterView, UserInfoView, UploadImageView, ChangePwdView, \
    MyCourseView, MyFavCourseView, MyFavTeacherView, MyFavOrgView, MyMessageView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),  # 当前app的专属urls配置文件
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('info/', UserInfoView.as_view(), name="info"),
    path('image/upload/', UploadImageView.as_view(), name="image"),
    path('update/pwd/', ChangePwdView.as_view(), name="pwd"),
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),
    # path('mycourse/', login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"),
    #                                  login_url="/user/login/"), {"current_page": "mycourse"}, name="mycourse"),
    path('myfavorg/', MyFavOrgView.as_view(), name="myfavorg"),
    path('myfavcourse/', MyFavCourseView.as_view(), name="myfavcourse"),
    path('myfavteacher/', MyFavTeacherView.as_view(), name="myfavteacher"),
    path('messages/', MyMessageView.as_view(), name="messages"),

]
