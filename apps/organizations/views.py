from django.shortcuts import render
from django.views.generic.base import View
from apps.organizations.models import CourseOrg, City, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.organizations.forms import AddAskForm
from django.http import JsonResponse
from apps.operations.models import UserFavorite


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
            "org_fav": org_fav,
            "hot_teachers": hot_teachers,
        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 对讲师进行排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")  # 负号表示倒序

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=10, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "hot_teachers": hot_teachers,
        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,
                                                                         fav_type=2):
            has_fav = True

        current_page = "desc"
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        current_page = "course"

        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,
                                                                         fav_type=2):
            has_fav = True

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=10, request=request)
        courses = p.page(page)

        return render(request, "org-detail-course.html", {
            "course_org": course_org,
            "all_courses": courses,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        current_page = "teacher"
        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,
                                                                         fav_type=2):
            has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "course_org": course_org,
            "all_teachers": all_teachers,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated and UserFavorite.objects.filter(user=request.user, fav_id=course_org.id,
                                                                         fav_type=2):
            has_fav = True
        current_page = "home"
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]  # 序列可能是空序列，这时候用[:1]取第一个元素是空，不会报错，而用[0]取则会报错。
        return render(request, "org-detail-homepage.html", {
            "course_org": course_org,
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class AddAskView(View):
    """
    处理用户我要学习咨询
    """

    def post(self, request, *args, **kwargs):
        userAskForm = AddAskForm(request.POST)
        if userAskForm.is_valid():
            user_ask = userAskForm.save(commit=True)
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '提交错误',
            })


class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_cities = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 通过机构类别对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构数据进行分页
        city_id = request.GET.get("city", "")
        if city_id and city_id.isdigit():
            all_orgs = all_orgs.filter(city_id=int(city_id))

        org_nums = all_orgs.count()

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")  # 负号表示倒序
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=10, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_cities,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
        })
