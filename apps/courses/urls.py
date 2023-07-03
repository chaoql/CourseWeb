from django.urls import path
from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView, VideoView

urlpatterns = [
    path('list/', CourseListView.as_view(), name="list"),  # 当前app的专属urls配置文件
    path("<int:course_id>/", CourseDetailView.as_view(), name="detail"),
    path("<int:course_id>/lesson/", CourseLessonView.as_view(), name="lesson"),
    path("<int:course_id>/comments/", CourseCommentsView.as_view(), name="comments"),
    path("<int:course_id>/video/<int:video_id>/", VideoView.as_view(), name="video"),
]
