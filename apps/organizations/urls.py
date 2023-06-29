from django.urls import path
from django.conf.urls import url
from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView


urlpatterns = [
    path('list/', OrgView.as_view(), name="list"),
    url(r'^add_ask', AddAskView.as_view(), name="add_ask"),
    # url(r'^(?P<org_id>\d+)', OrgHomeView.as_view(), name="home"),
    path("<int:org_id>/", OrgHomeView.as_view(), name="home"),
    path("<int:org_id>/teacher", OrgTeacherView.as_view(), name="teacher"),
    path("<int:org_id>/course", OrgCourseView.as_view(), name="course"),
    path("<int:org_id>/desc", OrgDescView.as_view(), name="desc"),

]