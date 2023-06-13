import xadmin
from apps.organizations.models import Teacher, CourseOrg, City


class CityAdmin(object):
    list_display = ["id", "name", "desc"]  # 定义列表页显示的字段
    search_fields = ["name", "desc"]  # 定义搜索的字段
    list_filter = ["name", "desc", "add_time"]  # 定义过滤器字段
    list_editable = ["name", "desc"]  # 定义允许在列表中直接编辑的字段


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    # relfield_style = 'fk-ajax'
    # style_fields = {"desc": "ueditor"}
    # model_icon = 'fa fa-university'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']
    # model_icon = 'fa fa-user-md'


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
