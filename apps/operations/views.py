from django.shortcuts import render
from django.views.generic import View
from apps.operations.models import UserFavorite, CourseComments
from apps.operations.forms import UserFavForm, CommentsForm
from django.http import JsonResponse
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher


class CommentView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            course = comments_form.cleaned_data["course"]
            comments = comments_form.cleaned_data["comments"]
            comment=CourseComments(user=request.user, comments=comments)
            comment.course = Course.objects.get(id=course.id)
            comment.save()
            return JsonResponse({
                "status":"success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误",
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录",
            })
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]
            # 是否收藏过
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    courseOrg = CourseOrg.objects.get(id=fav_id)
                    courseOrg.fav_nums -= 1
                    courseOrg.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "取消收藏",
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.user = request.user
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏",
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误",
            })
