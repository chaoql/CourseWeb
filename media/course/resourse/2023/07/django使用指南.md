# django使用指南

[toc]

## 1 初建项目

1. 创建项目

   django-admin startproject <项目名称>

2. 运行项目

   python manage.py runserver

3. 创建app

   python manage.py startapp <app名称>

4. 配置settings.py文件

   ```python
   STATICFILES_DIRS = [ # 共用一个static文件夹的话需要添加，使项目可以找到static文件静态资源(django可以自动在各个app下查找static资源)
       os.path.join(BASE_DIR, 'static')
   ]
   
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'templates')],# 添加，使项目可以找到templates文件静态资源
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
               ],
           },
       },
   ]
   ```


## 2 URL设置及管理

### 2.1 URL设置

1. 使用path()方法

   1. 导入app的url配置文件

      ```python
      from django.urls import path
      urlpatterns += [
          ......
          path("user/", include("apps.users.urls")),
      ]
      ```

   2. 关联类视图层

      ```python
      from django.urls import path
      urlpatterns += [
          ......
          path('list/', OrgView.as_view(), name="list"),    # 类视图后必须加as_view()
      ]
      ```

   3. 使用路径转换器获取URL链接中的数据

      > 路径转换器中获取数据参数包括：
      >
      > - `str` 匹配除了`/`之外的非空字符串；
      > - `int` 匹配0或者任何正整数，返回一个int；
      > - `slug` 匹配任意由ASCII字母或数字以及连字符和下划线组成的短标签；
      > - `path` 匹配非空字段，包括路径分隔符`/`。

      ```python
      from django.urls import path
      urlpatterns = [
          ......
          path("articles/<int:year>/", year_archive.as_view(), name="list"),
      ]
      ```

      如上述方式配置url后，当页面访问例如：`http://127.0.0.1:8000/articles/1/`这样的链接时会自动跳转到year_archive对应的视图类，并将`articles/`后的整型数据传递到get方法中，若要接收该数据则视图类应该在get方法中接受该参数，如下：

      ```python
      class year_archive(View):
          def get(self, request, year, *args, **kwargs):  # year一定要放在request参数之后
              pass
      ```

2. 使用url()方法

   url方法的使用和path方法几乎一致，但可以使用正则表达式匹配url，例如`path("<int:org_id>/", OrgHomeView.as_view(), name="home")`与`url(r'^(?P<org_id>\d+)', OrgHomeView.as_view(), name="home")`代码的功能完全一致。

### 2.2 URL管理

URL管理中，通常将各个app的url配置放在该app的目录下，最后在项目同名目录下的urls.py文件中统一导入。这样涉及到url命名空间的相关问题，具体可以参考[3 配置html页面显示](#3 配置html页面显示)章节中的内容。

### 2.3 URL传参

1. 方法一：

   > url格式为：`http://127.0.0.1:8000/org/list/?city=2&ct=pxjg`，将数据直接以键值对的方式传入后端，视图层以`category = request.GET.get("ct", "")`方式接收数据。

   ```django
   <a href="?city={{ city.id }}&ct={{ category }}"></a>
   ```

2. 方法二：

   > url格式为：`http://127.0.0.1:8000/org/1/`，后面的`1/`是举例代码中的`org.id`值，是一个变量，后端通过路径转换器获取该数据并传到视图层。（路径转换器相关知识请看[URL设置](#2.1 URL设置)）

   ```django
   <a href="{% url 'org:home' org.id %}"></a>
   ```

## 3 配置html页面显示

> 拆分页面静态文件（css，js，images）放入static，html放入templates之下
>
> 1. 放在对应的app下（不需要配置settings.py的STATICFILES_DIRS ）
> 2. 放到全局的templates和static之下（需要配置settings.py的STATICFILES_DIRS）

1. 编写对应app的views逻辑

   ```python
   # <project>/apps/<app>/views.py
   from django.shortcuts import render
   from django.views.generic.base import View
   
   
   class LoginView(View):
       def get(self, request, *args, **kwargs):
           return render(request, "login.html")
   
       def post(self, request, *args, **kwargs):
           pass
   ```

2. app目录下新建一个urls.py，编写当前app视图的路由

   ```python
   # <project>/apps/<app>/urls.py
   from django.urls import path
   
   from . import views
   
   urlpatterns = [
       path('login/', views.LoginView.as_view(), name="login"),  # 当前app的专属urls配置文件
   ]
   ```

3. 配置项目同名目录下的urls.py

   ```python
   # <project>/<project>/urls.py
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
       path("user/", include(("apps.users.urls"), "users"), namespace="user"),  # 引入新的urls配置文件
   ]
   
   ```

4. 前端使用该url：{% url 'namespace:name' %} 

   ```django
   <a href="{% url 'user:login' %}">data</a>
   ```

5. 最后访问http://127.0.0.1:8000/user/login/即可查看该网页

## 4 数据库连接（MySQL）

1. setting.py配置

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'message',
           'USER': 'root',
           'PASSWORD': '159357',
           'HOST': '127.0.0.1',
           'PORT': 3306,
           'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"}
       }
   }
   ```

2. 项目同名init.py配置

   ```python
   import pymysql
   
   pymysql.install_as_MySQLdb()
   ```

## 5 数据库操作

### 5.1 数据库设计

#### 5.1.1 表结构设计

1. 设计表

   ```python
   from django.db import models
   
   
   class Course(models.Model):
       """
       课程类模型
       """
       ......
       # on_delete参数表示对应的外键被删除后，当前数据应该怎么办？CASCADE表示级联删除，SET_NULL表示设置为空
       course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True, on_delete=models.CASCADE)
       name = models.CharField(max_length=50, verbose_name="课程名")
       learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
       degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")),
                                 max_length=2)
       image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
   
       class Meta:
           verbose_name = "课程信息"
           verbose_name_plural = verbose_name
   
       def __str__(self):
           return self.name
   ```

2. 生成数据库迁移文件

   ```
   python manage.py makemigrations
   ```

3. 将迁移文件集同步到数据库中

   ```
   python manage.py migrate
   ```

#### 5.1.2 数据类型

- models.AutoField

  >自增列 = int(11)
  >如果没有的话，默认会生成一个名称为 id 的列
  >如果要显式的自定义一个自增列，必须设置primary_key=True。

- models.CharField

  > 字符串字段
  > 必须设置max_length参数

- models.BooleanField

  >布尔类型=tinyint(1)
  >不能为空，可添加Blank=True

- models.ComaSeparatedIntegerField

  >用逗号分割的数字=varchar
  >继承CharField，所以必须 max_lenght 参数

- models.DateField

  >日期类型 date
  >DateField.auto_now：保存时自动设置该字段为现在日期，最后修改日期
  >DateField.auto_now_add：当该对象第一次被创建是自动设置该字段为现在日期，创建日期。

- models.DateTimeField

  >日期时间类型 datetime
  >同DateField的参数

- models.Decimal

  >十进制小数类型 = decimal
  >DecimalField.max_digits：数字中允许的最大位数
  >DecimalField.decimal_places：存储的十进制位数

- models.EmailField：一个带有检查 Email 合法性的 CharField

- models.FloatField：浮点类型 = double

- models.IntegerField：整形

- models.BigIntegerField：长整形

- models.GenericIPAddressField：一个带有检查 IP地址合法性的 CharField

- models.NullBooleanField：允许为空的布尔类型

- models.PositiveIntegerFiel：正整数

- models.PositiveSmallIntegerField：正smallInteger

- models.SlugField：减号、下划线、字母、数字

- models.SmallIntegerField

  >数字
  >
  >数据库中的字段有：tinyint、smallint、int、bigint

- models.TextField：大文本。默认对应的form标签是textarea。

- models.TimeField：时间 HH:MM[:ss[.uuuuuu]]

- models.URLField：一个带有URL合法性校验的CharField。

- models.BinaryField

  >二进制
  >
  >存储二进制数据。不能使用filter函数获得QuerySet。

- models.ImageField

  > 图片
  >
  > ImageField.height_field、ImageField.width_field：如果提供这两个参数，则图片将按提供的高度和宽度规格保存。
  >
  > 该字段要求 Python Imaging 库Pillow。
  >
  > 会检查上传的对象是否是一个合法图片。

- models.FileField(upload_to=None[, max_length=100, ** options])

  > 文件
  >
  > FileField.upload_to：一个用于保存上传文件的本地文件系统路径，该路径由 MEDIA_ROOT 中设置
  >
  > 这个字段不能设置primary_key和unique选项.在数据库中存储类型是varchar，默认最大长度为100

- models.FilePathField(path=None[, math=None, recursive=False, max_length=100, **options])

  > FilePathField.path：文件的绝对路径，必填
  >
  > FilePathField.match：用于过滤路径下文件名的正则表达式，该表达式将用在文件名上（不包括路径）。
  >
  > FilePathField.recursive：True 或 False，默认为 False，指定是否应包括所有子目录的路径。
  >
  > 例如：FilePathField(path="/home/images", match="foo.*", recursive=True)

#### 5.1.3 choices参数前端数据展示

例如[表结构设计](# 5.1.1 表结构设计)中的`degree`数据字段使用了`choices`参数简化存储，数据库中将使用`cj`代替`初级`来存储，在前端显示时却不能直接显示数据库中存储的`cj`数据。此时，有两种解决方案：

1. 使用`if`判断

   ```django
   {% if course.degree == 'cj' %}
       初级
   {% elif course.degree == 'zj' %}
       中级
   {% else %}
       高级
   {% endif %}
   ```

2. 使用`get_xxx_display`方法

   ```django
   {{ course.get_degree_display }}
   ```

### 5.2 数据查询

1. all()查询获取所有数据

   ```python
   from django.http import HttpResponse
   from django.shortcuts import render
   from apps.message_form.models import Message
   
   
   def message_form(request):
       all_messages = Message.objects.all()
       first_messages = Message.objects.all()[:1]  # 切片
       # 返回的是queryset对象，因此必须for遍历
       for message in all_messages:
           print(message.name)
       print(first_message.name)    
       return render(request, "message_form.html")
   ```

2. 查看执行的sql语句

   ```python
   def message_form(request):
       first_messages = Message.objects.all()[:1]
       print(first_message.query)  # 输出sql语句
       return render(request, "message_form.html")
   ```

3. filter()条件查询

   > get和filter的区别:
   >
   > - ### 返回值不同
   >
   >   - get的返回值是一个定义的model类的实例，即对象
   >   - filter的返回值是一个QuerySet的集合对象，可使用迭代或者遍历，切片等
   >
   > - ### 抛出异常不同
   >
   >   - get：只有一条记录返回的时候才正常。所以get多用于查询主键字段或者具有唯一性约束的字段，当有多条记录或者没有记录返回时，使用get均会抛出异常。
   >   - filter：没有记录、有一条或者多条记录返回均不会抛出异常。（没有记录的时候，返回值是一个空集合）

   ```python
   all_messages = Message.objects.filter(name="chaoql")
   # 返回的是queryset对象，因此必须for遍历
       for message in all_messages:
           print(message.email)
           
   message = Message.objects.get(name="chaoql")
   print(message.email)
   ```

4. get()获取一个数据对象

   ```python
   def message_form(request):
       # get()查询不到数据或查询到多条数据，则抛出异常
       try:
           message = Message.objects.get(name="chaoql1")
           print(message.address)
       except Message.DoesNotExist as e:
           pass
       except Message.MultipleObjectsReturned as e:
           pass
       return render(request, "message_form.html")
   ```

### 5.3 数据过滤

数据过滤指对查询出的结果筛掉其中不需要的部分，对queryset对象使用`exclude()`方法即可。

1. 筛掉其中一条数据

   ```python
   # 查询出Data数据表中除了id=1之外的其他数据
   data = Data.objects.all().exclude(id=1)
   ```

2. 筛掉多条数据

   ```python
   # 查询出Data数据表中除了id=1,2,3之外的其他数据
   data = Data.objects.all().exclude(id__in=[1, 2, 3])
   ```

3. 数据切片

   > 对queryset对象可以执行切片操作。
   >
   > 注意：[:1]和[0]都是表示第一个索引的元素，但一般使用[:1]，原因是有的序列可能是空序列，这时候用[:1]取第一个元素是空，不会报错，而用[0]取则会报错。

   ```python
   # 取前三个数据
   data = Data.objects.all()[:3]
   ```

### 5.4 数据删除

1. 删除get()到的数据对象

   ```python
   def message_form(request):
       try:
           message = Message.objects.get(name="chaoql1")
           print(message.address)
           message.delete()
       except Message.DoesNotExist as e:
           pass
       except Message.MultipleObjectsReturned as e:
           pass
   
       return render(request, "message_form.html")
   ```

2. 删除all()和filter()到的queryset数据

   ```python
   def message_form(request):
       all_messages = Message.objects.all()
       for message in all_messages:
           print(message.email)
           message.delete()  # 逐个数据对象删除
       all_messages.delete()  # 删除查询到的全部数据
       return render(request, "message_form.html")
   ```

### 5.5 数据插入/更新

```python
def message_form(request):
    # 初始化数据对象并提交
    message = Message()
    message.name = "chaoql"
    message.email = "1415331985@email.com"
    message.address = "西安"
    message.message = "无"
    # 数据提交：若数据存在则更新数据；若数据不存在则插入。（存在与否根据主键判别）
    message.save()
    return render(request, "message_form.html")
```

### 5.6 数据排序

```python
courses = courses.order_by("students")  # 对courses数据表以students字段为基准 正序排序
courses = courses.order_by("-students")  # 对courses数据表以students字段为基准 倒序排序
```

### 5.7 从前端界面POST数据到后端

```html
{# 前端页面表单部分 #}
<form action="/message_form/" method="post" class="smart-green">
    <h1>留言信息
        <span>请留下你的信息.</span>
    </h1>
    <label>
        <span>姓名 :</span>
        {# 后端会根据name属性提取数据 #}
        <input id="name" type="text" name="name" value="{{ message.name }}" class="error" placeholder="请输入您的姓名"/>
        <div class="error-msg"></div>
    </label>

    <label>
        <span>邮箱 :</span>
        <input id="email" type="email" value="{{ message.email }}" name="email" placeholder="请输入邮箱地址"/>
        <div class="error-msg"></div>
    </label>

    <label>
        <span>联系地址 :</span>
        <input id="address" type="text" value="{{ message.address }}" name="address" placeholder="请输入联系地址"/>
        <div class="error-msg"></div>
    </label>

    <label>
        <span>留言 :</span>
        <textarea id="message" name="message" placeholder="请输入你的建议">{{ message.message }}</textarea>
        <div class="error-msg"></div>
    </label>
    <div class="success-msg"></div>
    <label>
        <span>&nbsp;</span>
        <input type="submit" class="button" value="提交"/>
    </label>
    {# 安全验证机制，一定要添加这行代码！！！！！！ #}
    {% csrf_token %}
</form>
```

```python
# 后端逻辑部分
def message_form(request):
    if request.method == "POST":
        # 若访问该url的方式为“POST”，即提交表单时，执行以下操作
        message = Message()
        message.name = request.POST.get("name", "")
        message.email = request.POST.get("email", "")
        message.address = request.POST.get("address", "")
        message.message = request.POST.get("message", "")
        message.save()
    return render(request, "message_form.html")
```

### 5.8 传递数据到前端并显示

1. 视图层开发

   ```python
   class TestView(View):
       def get(self, request, *args, **kwargs):
           """
           获取课程列表信息
           """
           data = "data"
           return render(request, "template.html", {
               "data": data,
           })
   ```

2. 模板层开发

   前端页面直接使用`{{ data }}`即可显示数据。

### 5.9 重写模型类

1. 重写USER模型类，继承于AbstractUser类

   ```python
   # models.py
   
   from django.db import models
   from django.contrib.auth.models import AbstractUser
   
   
   GENDER_CHOICES = (
       ("male", "男"),
       ("famale", "女")
   )
   
   
   class UserProfile(AbstractUser):
       """
       重写用户模型类，继承自 AbstractUser
       """
       nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
       birthday = models.DateField(verbose_name="生日", null=True, blank=True)
       gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)
       address = models.CharField(max_length=100, verbose_name="地址", default="")
       mobile = models.CharField(max_length=11, unique=True, verbose_name="电话号码")
       image = models.ImageField(upload_to="head_image/%Y%m", default="default.jpg")
   
       class Meta:
           """
           对当前表进行相关设置
           """
           verbose_name = "用户信息"
           verbose_name_plural = verbose_name
   
       def __str__(self):
           """返回一个对象的描述信息"""
           if self.nick_name:
               return self.nick_name
           else:
               return self.username
   ```

2. 在setting.py文件中设置重写的用户模型类位置

   ```python
   AUTH_USER_MODEL = "user.UserProfile" 
   ```

### 5.10 创建并继承抽象父类

1. 创建父类模型

   ```python
   class BaseModel(models.Model):
       """
       用于存放多个模型共用的数据列，且不生成该类的数据表
       """
       add_time = models.DateTimeField(default=datetime.now, verbose_name="数据添加时间")
   
       class Meta:
           # 防止父类建表
           abstract = True
           
   ```

2. 继承该类

   ```python
   class Course(BaseModel):
       """
       课程类模型
       """
       name = models.CharField(max_length=50, verbose_name="课程名")
       
       class Meta:
           verbose_name = "课程信息"
           verbose_name_plural = verbose_name
       class __str__(self):
           return self.name  # 在print（实例）的时候返回你指定的字符串
   ```
   

### 5.11 数据表缓存静态资源文件

1. 配置settings.py

   ```python
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   MEDIA_URL = "/media/"
   ```

2. 建表

   ```python
   class CourseOrg(BaseModel):
       ......
       image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
   
       class Meta:
           ......
   ```

3. 这样上传的文件就会自动保存在`media`目录下的`org/%Y/%m`目录中。

4. 配置上传文件的访问地址

   ```python
   from django.views.static import serve
   from CourseWeb.settings import MEDIA_ROOT
   urlpatterns = [
       ......
       # 配置上传文件的访问url
       url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
   ]
   ```

5. 传递media全局变量到所有的html文件

   ```python
   TEMPLATES = [
       {
           'BACKEND': 'django.template.backends.django.DjangoTemplates',
           'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
           'APP_DIRS': True,
           'OPTIONS': {
               'context_processors': [
                   'django.template.context_processors.debug',
                   'django.template.context_processors.request',
                   'django.contrib.auth.context_processors.auth',
                   'django.contrib.messages.context_processors.messages',
                   'django.template.context_processors.media'  # here
               ],
           },
       },
   ]
   ```

6. 前端可以直接使用`MEDIA_URL`变量

   ```django
   两种方式均可显示静态资源
   src="{{MEDIA_URL}}{{course.image}}"
   
   src="{{course.image.url}}"
   ```

### 5.12 通过外键反取数据

> 假设课程数据表含有外键名为`课程机构id`，该外键是课程机构数据表的主键，现在有需求：取出课程机构A的所有课程。

在课程机构模型对象中建立courses(self)函数：

方法1：存在相互引用头文件的问题

```python
def courses(self):  # self为课程机构对象
    from apps.courses.models import Course
    courses = Course.objects.filter(course_org=self)
    return courses
```

方法2：通过外键反取数据

> 或者在前端直接`{{course_org.course_set.all}}`即可通过外键获取数据，若要获取数量则`{{course_org.course_set.all.count}}`

```python
def courses(self):  # self为课程机构对象
    courses = self.course_set.all()
    return courses
```

## 6 使用xadmin构建后台管理系统

### 6.1 配置xadmin

1. 在github搜索xadmin并下载源码

2. 在setting的INSTALLED_APPS中添加crispy_forms、xadmin、reversion、crispy_bootstrap3和django.conf，并配置语言和时区。

   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'apps.users.apps.UsersConfig',
       'apps.courses.apps.CoursesConfig',
       'apps.operations.apps.OperationsConfig',
       'apps.organizations.apps.OrganizationsConfig',
       'crispy_forms',
       'xadmin.apps.XAdminConfig',
       'reversion',
       'crispy_bootstrap3',
       'django.conf',
   ]
   CRISPY_TEMPLATE_PACK = 'bootstrap3'
   
   LANGUAGE_CODE = 'zh-hans'  # 配置显示为中文
   
   TIME_ZONE = 'Asia/Shanghai'  # 配置时区
   USE_TZ = False
   ```

3. 安装xadmin的依赖

   ```python
   pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt
   ```

4. 生成数据表并注册超级用户

   ```python
   makemigrations
   migrate
   createsuperuser
   ```

5. 配置urls.py

   ```python
   from django.contrib import admin
   from xadmin.plugins import xversion
   from django.urls import path
   import xadmin
   xversion.register_models()
   xadmin.autodiscover()
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('xadmin/', xadmin.site.urls),
   ]
   ```

### 6.2 注入app的数据表

1. 在app目录下新建adminx.py文件，并编辑如下：

   ```python
   import xadmin
   from apps.courses.models import City
   
   
   class CourseAdmin(object):
       """
       为每个需要注入的数据表创建Admin函数
       """
       list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 定义列表页显示的字段
       search_fields = ['name', 'desc', 'detail', 'degree', 'students']  # 定义搜索的字段
       list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 定义过滤器字段('外键__外键属性'：这种格式可以直接定位到外键属性)
       list_editable = ["degree", "desc"]  # 定义允许在列表中直接编辑的字段
   
   xadmin.site.register(Course, CourseAdmin)  # 注册数据表
   ```

2. 修改在xadmin网页中显示的该app名称（编辑app目录下的apps.py）

   ```python
   from django.apps import AppConfig
   
   
   class CoursesConfig(AppConfig):
       name = 'apps.courses'
       verbose_name = "课程管理"  # 别称
   ```

### 6.3 配置后台管理系统样式

```python
class GlobalSettings(object):
    site_title = "CW后台管理系统"  # 定义后台系统主题名称
    site_footer = "CW网站页脚"  # 定义后台系统网站页脚
    menu_style = "accordion"  # 左侧导航栏收起

class BaseSettings(object):
    enable_themes = True  # 允许更换主题皮肤配置
    use_bootswatch = True
    
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
```

## 7 form表单验证

> 对前端以POST方式传回后端的数据，使用django内置的form表单模块进行验证。

1. 创建表单的一般方法

   ```python
   from django import forms
   class LoginForm(forms.Form):
       """
       实现表单验证功能
       """
       username=forms.CharField(required=True, min_length=2)# 变量名必须与前端name标签保持一致
       password=forms.CharField(required=True, min_length=6)
   ```

2. 使用modelform创建表单

   > 使用model模型类直接创建form表单，其中UserAsk模型类定义如下：
   >
   > ```python
   > class UserAsk(BaseModel):
   >     name = models.CharField(max_length=20, verbose_name="姓名")
   >     mobile = models.CharField(max_length=11, verbose_name="手机")
   >     course_name = models.CharField(max_length=50, verbose_name="课程名")
   >     ......
   > ```

   ```python
   from django import forms
   from apps.operations.models import UserAsk
   
   class AddAskForm(forms.ModelForm):
       mobile = forms.CharField(required=True, min_length=11, max_length=11) 
       class Meta:
           model = UserAsk
           fields = ['name', 'mobile', 'course_name']
   ```

   使用modelform创建的表单在视图层提交到数据库是很方便，如下：

   ```python
   class AddAskView(View):
       """
       处理用户我要学习咨询
       """
       def post(self, request, *args, **kwargs):
           userAskForm = AddAskForm(request.POST)  # 初始化form对象
           if userAskForm.is_valid():
               user_ask = userAskForm.save(commit=True)  # 已提交到数据库
               ......
           else:
               ......
   ```

3. 使用clean方法对表单项进行自定义验证

   > clean_字段名()方法仅触发对单个字段的验证；
   >
   > clean()方法可以对多个字段进行验证。

   ```python
   class AddAskForm(forms.ModelForm):
       mobile = forms.CharField(required=True, min_length=11, max_length=11)
   
       class Meta:
           model = UserAsk
           fields = ['name', 'mobile', 'course_name']
   
       def clean_mobile(self):
           """
           验证手机号码是否合法
           :return:
           """
           mobile = self.cleaned_data['mobile']
           regex_mobile = '^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$'
           p = re.compile(regex_mobile)
           if p.match(mobile):
               return mobile
           else:
               raise forms.ValidationError('手机号码非法', code='mobile_invaild')
   ```

4. 视图层中使用表单验证模块

   ```python
   register_post_form = RegisterPostForm(request.POST)
   if register_post_form.is_valid():  # 在这行代码中会执行对表单数据的验证（包括clean方法）
       email = register_post_form.cleaned_data["email"]  # 表单中的数据都放在cleaned_data中
       password = register_post_form.cleaned_data["password"]
   ```

5. 模板层中显示form返回的errors

   ```django
   {% if register_post_form.errors %}
       {% for key, error in register_post_form.errors.items %}
           {{ error }}
       {% endfor %}
   {% else %}
       {{ msg }}
   {% endif %}
   ```


## 8 可复用登陆/注册功能模块开发

登陆和注册所使用的数据类都是用户数据类，其定义如下：

```python
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ("male", "男"),
    ("famale", "女"),
)


class BaseModel(models.Model):
    """
    用于存放多个模型共用的数据列，且不生成该类的数据表
    """
    add_time = models.DateTimeField(default=datetime.now, verbose_name="数据添加时间")

    class Meta:
        # 防止父类建表
        abstract = True


class UserProfile(AbstractUser):
    """
    重写用户模型类，继承自 AbstractUser
    """
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    # mobile = models.CharField(max_length=11, unique=True, verbose_name="电话号码")
    mobile = models.CharField(max_length=11, verbose_name="电话号码")
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y%m", default="default.jpg")

    class Meta:
        """
        对当前表进行相关设置
        """
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        """返回一个对象的描述信息"""
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
```

### 8.1 账户密码登录功能开发

1. 配置urls.py

   ```python
   from apps.users.views import LoginView, LogoutView
   urlpatterns = [
       path('login/', LoginView.as_view(), name="login"),  # 当前app的专属urls配置文件
       path('logout/', LogoutView.as_view(), name="logout"),
   
   ]
   ```

2. 视图层开发

   ```python
   from django.shortcuts import render
   from django.views.generic.base import View
   from django.contrib.auth import authenticate, login, logout
   from django.http import HttpResponseRedirect
   from django.urls import reverse
   
   from apps.operations.models import UserProfile
   from apps.users.forms import LoginForm, DynamicLoginForm, RegisterGetForm, RegisterPostForm
   
   
   class LoginView(View):
       def get(self, request, *args, **kwargs):
           if request.user.is_authenticated:
               return HttpResponseRedirect(reverse("index"))
           return render(request, "login.html")
   
       def post(self, request, *args, **kwargs):
           login_form = LoginForm(request.POST)  # 创建表单用于验证数据以及获取数据
           if login_form.is_valid():
               user_name = login_form.cleaned_data["username"]
               password = login_form.cleaned_data["password"]
   
               # 表单验证
               if not user_name:
                   return render(request, "login.html", {"msg": "请输入用户名"})
               if not password:
                   return render(request, "login.html", {"msg": "请输入密码"})
               
               # 用户查询（通过用户名和加密后的密码）
               user = authenticate(username=user_name, password=password)
               if user is not None:
                   login(request, user)
                   # 重定向url，调用reverse函数通过urlname来反向解析url
                   return HttpResponseRedirect(reverse("index"))
               else:
                   return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
           else:
               return render(request, "login.html", {"login_form": login_form})
   ```

3. 表单验证

   ```python
   from django import forms
   
   
   class LoginForm(forms.Form):
       """
       实现表单验证功能
       """
       username=forms.CharField(required=True, min_length=2)# 变量名必须与前端name标签保持一致
       password=forms.CharField(required=True, min_length=6)
   ```

4. 模板层开发

   ```html
   <div class="fl form-box">
       <h2>帐号登录</h2>
       <form action="{% url 'login' %}" method="post" autocomplete="off">
           <input type='hidden' name='csrfmiddlewaretoken' value='mymQDzHWl2REXIfPMg2mJaLqDfaS1sD5'/>
           <div class="form-group marb20 {% if login_form.errors.username %}errorput{% endif %}">
               <label>用&nbsp;户&nbsp;名</label>
               <input name="username" id="account_l" type="text" placeholder="手机号/邮箱"
                      value="{{ login_form.username.value }}"/>
           </div>
           <div class="form-group marb8 {% if login_form.errors.password %}errorput{% endif %}">
               <label>密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</label>
               <input name="password" id="password_l" type="password" placeholder="请输入您的密码"
                      value="{{ login_form.password.value }}"/>
           </div>
           <div class="error btns login-form-tips" id="jsLoginTips">
               {% if login_form.errors %}
                   {% for key, error in login_form.errors.items %}
                       {{ error }}
                   {% endfor %}
               {% else %}
                   {{ msg }}
               {% endif %}
           </div>
           <div class="auto-box marb38">
   
               <a class="fr" href="forgetpwd.html">忘记密码？</a>
           </div>
           <input class="btn btn-green" id="jsLoginBtn" type="submit" value="立即登录 > "/>
           <input type='hidden' name='csrfmiddlewaretoken' value='5I2SlleZJOMUX9QbwYLUIAOshdrdpRcy'/>
           {% csrf_token %}
       </form>
       <p class="form-p">没有慕学在线网帐号？<a href="register.html">[立即注册]</a></p>
   </div>
   ```

### 8.2 注册功能开发

1. 配置urls.py

   ```python
   urlpatterns += [
       ······
       path('register/', RegisterView.as_view(), name="register"),
   ]
   ```

2. 视图层开发

   ```python
   class RegisterView(View):
       def get(self, request, *args, **kwargs):
           register_get_form = RegisterGetForm()
           return render(request, "register.html", {
               "register_get_form": register_get_form,
           })
   
       def post(self, request, *args, **kwargs):
           register_post_form = RegisterPostForm(request.POST)
           if register_post_form.is_valid():
               email = register_post_form.cleaned_data["email"]
               password = register_post_form.cleaned_data["password"]
               user = UserProfile(username=email, email=email)
               user.set_password(password)
               user.save()
               login(request, user)
               return HttpResponseRedirect(reverse("index"))
           else:
               register_get_form = RegisterGetForm()
               return render(request, "register.html", {
                   "register_get_form": register_get_form,
                   "register_post_form": register_post_form,
               })
   ```

3. form表单验证

   ```python
   class RegisterGetForm(forms.Form):
       captcha = CaptchaField()
   
   
   class RegisterPostForm(forms.Form):
       captcha = CaptchaField()
       email = forms.EmailField(required=True)  # 变量名必须与前端name标签保持一致
       password = forms.CharField(required=True, min_length=6)
   
       def clean_email(self):
           email = self.data.get("email")
           users = UserProfile.objects.filter(email=email)
           if users:
               raise forms.ValidationError("该邮箱已注册")
           return email
   ```

4. 模板层开发

   ```python
   <form id="email_register_form" method="post" action="{% url 'register' %}" autocomplete="off">
       <div class="form-group marb20 {% if register_post_form.errors.email %}errorput{% endif %}">
           <label>邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱</label>
           <input type="text" id="id_email" name="email" value="{{ register_post_form.email.value }}"
                  placeholder="请输入您的邮箱地址"/>
       </div>
       <div class="form-group marb8 {% if register_post_form.errors.password %}errorput{% endif %}">
           <label>密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</label>
           <input type="password" id="id_password" name="password"
                  value="{{ register_post_form.password.value }}"
                  placeholder="请输入6-20位非中文字符密码"/>
       </div>
       <div class="form-group marb8 captcha1 ">
           <label>验&nbsp;证&nbsp;码</label>
           {{ register_get_form.captcha }}
       </div>
       <div class="error btns" id="jsEmailTips"></div>
       {% if register_post_form.errors %}
           {% for key, error in register_post_form.errors.items %}
               {{ error }}
           {% endfor %}
       {% else %}
           {{ msg }}
       {% endif %}
       <div class="auto-box marb8">
       </div>
       <input class="btn btn-green" id="jsEmailRegBtn" type="submit" value="注册并登录"/>
       {% csrf_token %}
   </form>
   ```

## 9 图形验证码

### 9.1 安装配置

1. 安装第三方库

   ```
   pip install django-simple-captcha
   ```

2. 配置settings.py

   ```python
   INSTALLED_APPS = [
   	......
       'captcha',
   ]
   ```

3.  将已存在的数据库迁移文件集同步到数据库中

   ```
   python manage.py migrate
   ```

4. 配置urls.py:

   ```python
   urlpatterns += [
       path('captcha/', include('captcha.urls')),
   ]
   ```

### 9.2 验证码显示及正确性验证

> 注意：请将代码中的\<form\>替换为传入前端的form表单名称

1. 验证码显示
   1. 将`captcha = CaptchaField()`写入forms.py；
   2. 在前端显示图形验证码的位置输入：`{{ <form>.captcha }}`。
2. 正确性验证时不需要在form表单中创建局部钩子，其验证会包含在视图层中的`<form>.is_valid()`中完成。

## 10 template模板层

### 10.1 基础操作

1. for循环

   1. 格式

      ```django
      {% for i in data%}
      {% endfor %}
      ```

   2. 显示for循环轮数

      ```django
      {% for org in hot_orgs %}
      	<dt class="num fl">循环到第{{ forloop.counter }}轮</dt>
      {% endfor %}
      ```

2. if判断

   ```django
   {# if一般写法 #}
   {% if data == "1" %}
   {% endif %}
   {# 使用ifequal关键字完成判断 #}
   {% ifequal data "1" %}
   {% endifequal %}
   ```

3. 前端数据由整数转换为字符串类型

   ```django
   {% data|stringformat:'i' %}
   ```

4. 使用后端传来的类的属性和函数

   类的属性和函数的使用方法一样，前端都将其看作是一个属性，因此`{{ class.function }}`即可。

### 10.2 使用template的static引入静态文件 

1. 配置setting.py

   ```python
   STATIC_URL = '/static/'  # 前端template引入静态文件的路径
   ```

2. 在前端加载静态接口

   ```django
   {% load static %}
   ```

3. 引入静态文件

   ```django
   "{% static 'js/jquery.min.js' %}"
   ```

### 10.3 temolate根据路由别名执行路由规则url

1. 在urls.py配置路由时设置路由别名

   ```python
   urlpatterns = [
       path('login/', LoginView.as_view(), name="login"), 
   ]
   ```

2. 前端引用该url

   ```django
   {% url 'login' %}
   ```

### 10.4 前端模板base.html继承

1. 编写base.html：

   1. 复制一个html页面；
   2. 把其他页面将替换的部分都放在block里；
   3. 保留网页header和footer，block中的内容都删掉；

   ```html
   <!DOCTYPE html>
   <html>
   {% load static %}
   <head>
       <meta charset="UTF-8">
       <meta name="renderer" content="webkit">
       <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
       <title>{% block title %}首页 - 在线教育平台{% endblock %}</title>
       <link rel="stylesheet" type="text/css" href="{% static 'css/reset.css' %}">
       <link rel="stylesheet" type="text/css" href="{% static 'css/animate.css' %}">
       <link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">
       {% block custom_css %}
       {% endblock %}
       <script src="{% static 'js/jquery.min.js' %}" type="text/javascript"></script>
       <script src="{% static 'js/jquery-migrate-1.2.1.min.js' %}" type="text/javascript"></script>
   
   </head>
   <body>
   <section class="headerwrap ">
       <header>
           ......
       </header>
   </section>
   
   {% block custom_bread %}
   {% endblock %}
   
   {% block content %}
   {% endblock %}
   
   <footer>
       ......
   </footer>
   
   <section>
       <ul class="sidebar">
           <li class="qq">
               <a target="_blank" href="http://wpa.qq.com/msgrd?v=3&uin=2023525077&site=qq&menu=yes"></a>
           </li>
           <li class="totop"></li>
       </ul>
   </section>
   <script src="{% static 'js/selectUi.js' %}" type='text/javascript'></script>
   <script src="{% static 'js/.js' %}" type='text/javascript'></script>
   <script type="text/javascript" src="{% static 'js/plugins/laydate/laydate.js' %}"></script>
   <script src="{% static 'js/plugins/layer/layer.js' %}"></script>
   <script src="{% static 'js/plugins/queryCity/js/public.js' %}" type="text/javascript"></script>
   <script src="{% static 'js/unslider.js' %}" type="text/javascript"></script>
   <script src="{% static 'js/plugins/jquery.scrollLoading.js' %}" type="text/javascript"></script>
   <script src="{% static 'js/deco-common.js' %}" type="text/javascript"></script>
   
   {% block custom_js %}
   {% endblock %}
   </body>
   </html>
   ```

2. 在其他页面继承base.html

   1. 继承base.html

      ```django
      {% extends 'base.html' %}
      ```

   2. 对父模板中的block内容进行填充

      ```html
      {% extends 'base.html' %}
      {% block title %}机构列表页 - 在线教育平台{% endblock %}
      {% block custom_bread %}
      ......
      {% endblock %}
      
      {% block content %}
      ......
      {% endblock %}
      
      {% block custom_js %}
      ......
      {% endblock %}
      ```


### 10.5 分页功能实现

1. 安装第三方依赖

   ```
   pip install django-pure-pagination
   ```

2. 配置setting.py

   ![](.\687474703a2f2f692e696d6775722e636f6d2f4c437172742e676966.gif)

   ```python
   INSTALLED_APPS = (
       ...
       'pure_pagination',
   )
   
   PAGINATION_SETTINGS = {
       'PAGE_RANGE_DISPLAYED': 10,
       'MARGIN_PAGES_DISPLAYED': 2,
   
       'SHOW_FIRST_PAGE_WHEN_INVALID': True,
   }
   ```

3. 视图层view.py

   ```python
   class OrgView(View):
       def get(self, request, *args, **kwargs):
           all_orgs = CourseOrg.objects.all()
   		
           ......
           
           # 对课程机构数据进行分页
           try:
               page = request.GET.get('page', 1)
           except PageNotAnInteger:
               page = 1
           # per_page参数控制每页显示多少数据
           p = Paginator(all_orgs, per_page=10, request=request)
           orgs = p.page(page)
   
           return render(request, "org-list.html", {
               "all_orgs": orgs,
               ......
           })
   ```

4. 模板层template.html

   > 注意：使用分页功能后，传到前端的数据若要进行for循环，则必须使用object_list方法，如：`{% for org in all_orgs.object_list %}`

   ```python
   <div class="pageturn">
       <ul class="pagelist">
           {% if all_orgs.has_previous %}
               <li class="long"><a href="?{{ all_orgs.previous_page_number.querystring }}">上一页</a></li>
           {% endif %}
           {% for page in all_orgs.pages %}
               {% if page %}
                   {% ifequal page all_orgs.number %}
                       <li class="active"><a href="?{{ page.querystring }}">{{ page }}</a></li>
                   {% else %}
                       <li><a href="?{{ page.querystring }}" class="page">{{ page }}</a></li>
                   {% endifequal %}
               {% else %}
                   <li class="none">...</li>
               {% endif %}
           {% endfor %}
           {% if all_orgs.has_next %}
               <li class="long"><a href="?{{ all_orgs.next_page_number.querystring }}">下一页</a></li>
           {% endif %}
       </ul>
   </div>
   ```

### 10.6 前端获取当前页面名称

这个功能乍一看有些鸡肋，但实际上对于某些功能的实现却不可或缺。例如：当你要在前端页面导航栏众多标签中高亮某一标签以提示用户处于哪个页面，那么你得让前端知道当前页面是哪个页面，才能高亮具体的标签。有两种实现方式：

1. 视图层传值到前端

   1. 视图层开发

      ```python
      class TestView(View):
          def get(self, request, *args, **kwargs):
              """
              获取课程列表信息
              """
              current_page = "course"
              return render(request, "course-list.html", {
                  "current_page": current_page,
              })
      ```

   2. 模板层开发

      ```django
      {% if current_page == 'course' %}
      ......
      {% endif %}
      ```

2. 前端对request.path切片获得

   ```django
   {% if request.path == '/' %}{% endif %}
   
   {% if request.path|slice:'7' == '/course' %}{% endif %}
   ```

## 11 其他应用操作

### 11.1 控制view必须登录才能访问

使用登录装饰器即可完成

```python
from django.contrib.auth.mixins import LoginRequiredMixin


class MyView(LoginRequiredMixin, View):
    login_url = "/login/"  # 设置登录的url
    def get(self, request, *args, **kwargs):
        pass
```

### 11.2 登陆后跳转回原页面

使用登录装饰器验证用户是否登录后，若用户未登录则跳转至登陆界面，且会在url后以`next`参数形式添加原页面的url地址，如：`http://127.0.0.1:8000/user/login/?next=/course/4/lesson/`。（如果不是登录装饰器自动添加，那也可以自己添加，完成该步骤）

1. 在登录类的get方法中获取`next`参数的数值，并传入前端。

   > 对这种传参方式不了解的话请看[URL传参](#2.3 URL传参)。

   ```python
   class LoginView(View):
   	def get(self, request, *args, **kwargs):
           ......
           # 在get方法中获取原页面地址
           next = request.GET.get("next", "")
           return render(request, "login.html", {
               "next": next,
           })
   
       def post(self, request, *args, **kwargs):
           ......
   ```

2. 前端form表单获取get传入的`next`参数值，并将其发往后端登陆类的post方法

   ```django
   <form action="{% url 'login' %}?next={{ next }}" method="post" autocomplete="off">
   </form>
   ```

3. 登陆类的post方法接收该数据并在验证登陆成功后重定向到该页面

   ```python
   class LoginView(View):
   	def get(self, request, *args, **kwargs):
           ......
   	def post(self, request, *args, **kwargs):
           ......
   		next = request.GET.get("next", "")
   		if next:
   			return HttpResponseRedirect(next)
   ```

   







 



