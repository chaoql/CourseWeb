from django.contrib import admin
from xadmin.plugins import xversion
from django.urls import path, include
import xadmin
from django.views.generic import TemplateView
from apps.users.views import LoginView

xversion.register_models()
xadmin.autodiscover()
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path("", include("apps.users.urls")),  # 引入新的urls配置文件
    path('captcha/', include('captcha.urls')),  # 图形验证模块的urls配置文件
]
