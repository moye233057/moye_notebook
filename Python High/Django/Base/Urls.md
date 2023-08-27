一、URL
* 定义：统一资源定位符 Uniform Resource Locator
* 作用：用来表示互联网上某个资源的地址
* URL的一般语法格式为([]代表其中的内容可省略)：
  * protocol://hostname[:port]/path[?query][#fragment]
  * protocol（协议）
    * http通过HTTP访问该资源。格式http://
    * https通过安全的HTTPS访问资源。格式https://
    * file资源是本地计算机上的文件。格式file:///
  * hostname（主机名）
    * 指存放资源的服务器的域名系统（DNS）主机名、域名或IP地址
  * port（端口号）
    * 整数，可选，省略时使用80作为默认端口
    * 各种传输协议都有默认端口号，如http默认端口号为80
  * path (路由地址)
    * 由零或多个“/”符号隔开的字符串，一般用来表示主机上的一个目录或文件地址。路由地址决定了服务器端如何处理这个请求
  * query（查询）
    * 可选，用于给动态网页传递参数，可多个，用“&”符号隔开，每个参数的名和值用“=”符号隔开
  * fragment（信息断片）
    * 字符串，用于指定网络资源中的片段。例如一个网页中有多个名称解释，可使用fragment直接定位到某个名词解释
* URL通常与视图(View）一起工作的。服务器收到用户请求后，会根据urls.py里的关系条目，去视图View里查找到与请求对应的处理方法，从而返回给客户端http页面数据
* 当浏览器输入/blog/article/<int:id>/时，URL不仅调用了views.py里的article方法，而且还把参数文章id通过<>括号的形式传递给了视图。int这里代表只传递整数，传递的参数名字是id

二、处理URL请求
1. Django从配置文件中根据ROOT_URLCONF找到主路由文件；默认情况下，该文件在项目同名目录下的urls
2. Django加载主路由文件中的urlpartterns变量（包含很多路由的数组）
3. 依次匹配urlpatterns中的path，匹配第一个合适的路由，成功后中断后续匹配
4. 匹配成功，调用对应的视图函数处理请求，返回响应
5. 匹配失败，返回404响应

三、路由配置与视图函数Views
* 视图函数时用于接收一个浏览器请求（HttpRequest对象）并通过HttpResponse对象返回响应的函数。此函数可以接收浏览器请求并根据业务逻辑返回响应的响应内容给浏览器
* 路由配置
```
from django.urls import path

urlpatterns = [
    path(route, views, name=None)
]
# route:字符串类型，匹配的请求路径
# views:指定路径所对应的视图处理函数的名称
# name:为地址起别名，在模板中地址反向解析时使用

# path转换器
```
转换器类型 | 作用 | 样例
--- | --- | ---
str | 匹配除了'/'之外的非空字符串 | "v1/users/<str:username>"
int | 匹配0或任何正整数，返回一个int | "page/<int:page>"
slug | 匹配任意由ASCII字母或数字以及连字符和下划线组成的短标签 | "detail/<sl>" 匹配 /detail/this-is-django
path | 匹配非空字段，包括路径分隔符"/" | "v1/users/<path:ph>" 匹配 /v1/goods/a/b/c 

语法：<转换器类型:自定义名>
作用：若转换器类型匹配到对应类型的数据，则将数据按照关键字传参的方式传递给视图函数
例子：path("page/<int:page>", views.xxx)
def xxx(request, page)：
    html = ""
    return HttpResponse(html)

re_path 正则匹配
* 作用：在url的匹配过程中可以使用正则表达式进行精确匹配
* 语法：re_path(reg, view, name=xxx)
* 正则表达式为命名分组模式（?P<name>pattern）;匹配提取后用关键字传参的方式传递给视图函数

通过URL方法传递额外的参数
* 在配置URL时，还可以通过字典的形式传递额外的参数给视图, 而不用把这个参数写在链接里
* 例如：
```
urlpatterns = [
path('', views.ArticleList.as_view(), name='article_list', {'blog_id': 3}),
re_path(r'^blog/article/(?P<id>\d+)/$', views.article, name='article'),
]
```

四、分布式路由
* Django中，主路由配置文件（urls.py）可以不处理用户具体路由，主路由配置文件可以做请求的分发。具体的请求由各自的应用进行处理
* 配置：
  1. 主路由中调用include函数
    * 语法：include('app名字.url模块名')
    * 作用：用于将当前路由转到各个应用的路由配置文件urlpatterns进行分布式处理
  2. 应用下配置urls.py，内容结果同主路由完全一样   
