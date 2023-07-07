from django.contrib import admin
from xadmin.plugins import xversion
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
import xadmin
from django.views.generic import TemplateView
from CourseWeb.settings import MEDIA_ROOT

xversion.register_models()
xadmin.autodiscover()
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),  # 类视图后必须加as_view()
    path("user/", include(("apps.users.urls",  "users"), namespace="user")),
    path("org/", include(("apps.organizations.urls", "organizations"), namespace="org")),
    path("op/", include(("apps.operations.urls", "operations"), namespace="op")),
    path("course/", include(("apps.courses.urls", "courses"), namespace="course")),
    path('captcha/', include('captcha.urls')),  # 图形验证模块的urls配置文件
    # 配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
