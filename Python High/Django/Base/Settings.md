### settings.py包含Django项目的所有配置项
* 配置项分为公有配置和自定义配置
* 配置项格式：BASE_DIR = 'xxx'

### 公有配置：Django官方提供的基础配置
* BASE_DIR:settings.py的上级目录的路径
* DEBUG:项目的启动模式，True为调试模式，False是上线模式
* ALLOW_HOSTS:允许的请求头
* ROOT_URLCONF:主路由
* INSTALLED_APPS:指定当前项目中安装的应用列表
* MIDDLEWARE:用于注册中间件
* TEMPLATES:用于指定模板的配置信息
* DATABASES:用于指定数据库的配置信息
* LANGUAGE_CODE:用于指定语言配置

### 实战配置
#### APP注册配置（django2.0及以后）
```
# 为了方便项目的app管理，会将所有的app统一存放在一个文件夹，例如apps
# 这时候在INSTALLED_APPS里面直接用app名称注册会找不到
# 需要在BASE_DIR下面加上
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# 这样就可以直接在INSTALLED_APPS里面用app名注册，例如
INSTALLED_APPS = [
    ...
    'user',
    ...
]
# 但是这样会出现一个问题，如果我们在views中引入模型model的时候，用apps.APP名.模型名的路径来引入
# 会出现报错RuntimeError: Model class apps.user.models.xxx doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
# 因为APP的路径已注册，所以正确的引用方式为：
APP名.模型名
# 例如：from user.models import Account

```

#### HOST头、跨域配置、请求方式、HTTP标头
```
# 允许的请求头HOST头
ALLOWED_HOSTS = ['*']
# 如果为True，则将允许将cookie包含在跨站点HTTP请求中。默认为False
CORS_ALLOW_CREDENTIALS = True
# 添加允许执行跨站点请求的主机
# 如果为True，则将不使用白名单，并且将接受所有来源。默认为False
CORS_ORIGIN_ALLOW_ALL = True
# 授权进行跨站点HTTP请求的来源列表。默认为[]
CORS_ORIGIN_WHITELIST = []
# 允许的HTTP请求方式
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
# 发出实际请求时可以使用的非标准HTTP标头的列表
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
```

#### 修改默认时区语言
```
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

#### 静态路径构建使admin后台的static/admin下的样式不失效
* 在settings.py下添加
```
STATIC_URL = '/static/'   # 静态文件的别名
STATIC_ROOT = 'static'    # DEBUG=False新增行
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '/static/')    # 'static' 改为 '/static/'
]
```
* 在settings.py同级的urls.py中的urlpatterns中添加
```
# 一般来说是在urlpatterns = []的后面添加 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
# 但是这种配置只能在settings.py中的debug=True的时候生效，如果变为False就会失效
# 需要当作普通路径添加：
from django.conf import settings
from django.conf.urls.static import static, serve
from django.urls import  re_path
urlpatterns = [
  re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
```
* 迁移django官方的样式文件到staticz中
```
# 经过上面步骤配置后，请求ip:port/static时，就能够访问到项目主目录下的static文件夹
# 运行django时，django需要的静态文件路径为ip:port/static/admin，这个admin文件的路径在pip install django安装时的django包里面，路径为:
# ubuntu系统：/usr/local/lib/python(版本号)/dist-packages/django/contrib/admin/static/admin  最后这个admin文件夹就是我们要复制到django项目static下的文件夹
# 其他系统可以找到对应的django这个包，admin主要存放的是官方的css、js、img文件
sudo cp -r /usr/local/lib/python3.5/dist-packages/django/contrib/admin/static/admin /project/static
```