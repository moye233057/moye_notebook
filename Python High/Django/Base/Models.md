### 概念
* Model (模型) 简而言之即数据模型。模型不是数据本身（比如数据库里的数据），而是抽象的描述数据的构成和逻辑关系
* 每个Django model实际上是个类，继承了models.Model。每个Model应该包括属性，关系（比如单对单，单对多和多对多）和方法
* 当你定义好Model模型后，Django的接口会自动帮你在数据库生成相应的数据表(table)

### Django配置mysql
* 安装python3-dev和default-libmysqlclient-dev
  * 查看：sudo apt list --installed|grep -E 'libmysqlclient-dev|python3-dev'
  * 安装：sudo apt-get install libmysqlclient-dev python3-dev
* 安装mysqlclient: sudo pip3 install mysqlclient
* 进入mysql数据库，创建数据库：create database 数据库名default charset utf8
* 通常数据库名与项目名保持一致
* settings.py里修改数据库配置DATABASES

### 定义Django模型Model的时候，一定要十分清楚2件事:
* 这个Field是否有必选项, 比如CharField的max_length和ForeignKey的on_delete选项是必须要设置的
* 这个Field是否必需(blank = True or False)，是否可以为空 (null = True or False)。这关系到数据的完整性
* 对于空白的CharField和TextField永远不会存为null空值，而是存储空白字符串''，正确的做法是设置default=''

### Django Model中字段(Field)的可选项和必选项
* 字符/文本字段
  * CharField() 字符字段
  max_length = xxx or None
  如不是必填项，可设置blank = True和default = ''
  如果用于username, 想使其唯一，可以设置unique = True
  如果有choice选项，可以设置 choices = XXX_CHOICES

  * TextField() 文本字段
  max_length = xxx
  如不是必填项，可设置blank = True和default = ''

  * 没有必要同时设置blank=True和null=True，原因如下。
  blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响。
  null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空，即在Null字段显示为yes。
  对于CharField和TextField，如果为空字符串或没有字符，数据库里会存储''空字符串，不会以null形式存储，所以设置nul=True没有任何意义。


* DateField() and DateTimeField() 日期与时间字段
一般建议设置默认日期default date.
For DateField: default=date.today - 先要from datetime import date
For DateTimeField: default=timezone.now - 先要from django.utils import timezone
对于上一次修改日期(last_modified date)，可以设置: auto_now=True

* EmailField() 邮件字段
如不是必填项，可设置blank = True和default = ''
一般Email用于用户名应该是唯一的，建议设置unique = True

* IntegerField(), SlugField(), URLField()，BooleanField()
可以设置blank = True or null = True
对于BooleanField一般建议设置defautl = True or False
FileField(upload_to=None, max_length=100) - 文件字段
upload_to = "/some folder/"
max_length = xxxx

* ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,)
upload_to = "/some folder/"
其他选项是可选的.

* ForeignKey(to, on_delete, **options) - 单对多关系
to必需指向其他模型，比如 Book or 'self' .
必需指定on_delete options（删除选项): i.e, "on_delete = models.CASCADE" or "on_delete = models.SET_NULL" .
可以设置"default = xxx" or "null = True" .
如果有必要，可以设置 "limit_choices_to = "，如下面例子。
staff_member = models.ForeignKey( User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, )
可以设置 "related_name = xxx" 便于反向查询。

* ManyToManyField(to, **options) - 多对多关系
to 必需指向其他模型，比如 User or 'self' .
设置 "symmetrical = False " if 多对多关系不是对称的
设置 "through = 'intermediary model' " 如果需要建立中间模型来搜集更多信息
可以设置 "related_name = xxx" 便于反向查询。

### 反向查询
* 对于ForeignKey字段（一对多），可以通过变量名_set的方式从多的模型反向查询到一的模型，存在不直观的问题
* 可以在模型里设置related_name= 就可以直接通过多model.related_name.一model变量来查询。注意一但设置了related name, 将不能再通过_set方法来反向查询