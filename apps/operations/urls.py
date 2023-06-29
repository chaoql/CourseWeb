from django.urls import path
from apps.operations.views import AddFavView

urlpatterns = [
    path('fav/', AddFavView.as_view(), name="fav"),  # 当前app的专属urls配置文件
]
