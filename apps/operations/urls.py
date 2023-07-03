from django.urls import path
from apps.operations.views import AddFavView, CommentView

urlpatterns = [
    path('fav/', AddFavView.as_view(), name="fav"),  # 当前app的专属urls配置文件
    path('comment/', CommentView.as_view(), name="comment"),  # 当前app的专属urls配置文件
]
