from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course, CourseTag, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operations.models import UserFavorite, UserCourse, CourseComments


class VideoView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        video = Video.objects.get(id=video_id)
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有同学还学过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=course.id).order_by(
            "-course__click_nums")[:5]
        related_courses = [userCourse.course for userCourse in all_user_courses]

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有同学还学过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=course.id).order_by(
            "-course__click_nums")[:5]
        related_courses = [userCourse.course for userCourse in all_user_courses]

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有同学还学过什么课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=course.id).order_by(
            "-course__click_nums")[:5]
        related_courses = [userCourse.course for userCourse in all_user_courses]

        course_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # 获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course.id,
                                                                         fav_type=1):
            has_fav_course = True
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,
                                                                         fav_type=2):
            has_fav_org = True
        # 通过课程的tag字段做课程的推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]
        # 通过coursetag表做课程推荐
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        related_courses = set()  # 去重
        for course_tag in course_tags:
            related_courses.add(course_tag.course)
        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取课程列表信息
        """
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]
        # 课程排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=10, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })
