### Cookie
#### 概念
* Cookie是保存在客户端（浏览器）中的键值对
* 存储的数据带有生命周期
* cookies中的数据是按域存储隔离的，不同的域之间无法访问
* cookies的内部的数据在每次访问此网址时，都会携带到服务器端，如果cookie过大会降低响应速度

#### Cookie 固有缺点：
* 本身最大支持 4096 字节
* Cookie 本身保存在客户端，可能被拦截或窃取
* 为了能支持更多的字节，并且保存在服务器，有较高的安全性。使用session

### Session
#### 概念
* Session是保存在服务端的键值对
  * 在服务器上开辟一段空间用于保留浏览器和服务器交互时的重要数据
  * Session 依赖于 Cookie，需要在浏览器客户端启动cookie，且在cookie中存储sessionid
  * 给每个客户端的 Cookie 分配一个唯一的 id 即 sessionid ，这样用户在访问时，通过Cookie，服务器就知道来的人是“谁”，不同请求者之间不会共享这个数据

#### 存储形式 
* django服务器上存储的Session
  *    格式: session_value :  {'is_login': 1, 'name': 'xiaoming', 'age': 18}
  * 是一个类似于字典的SessionStore类型的对象，可以用类似字典的方式操作
  * 能够存储字符串。整型，字典，列表等
  * Django 默认使用数据库存储 Session 数据。如果直接运行使用 Session 会报：no such table:django_session
  * 需要先用python manage.py makemigrations和python manage.py manage.py migrate进行迁移创建session的数据库表

* 浏览器中的Session格式  sessionid : session_value
  * 主流网页F12或鼠标右键检查（Inspect）调出浏览器开发者工具
  * 在>>中找到应用（application）
  * 在Storage中就能够找到sessionid

#### Django获取Session数据的过程
* 从用户发来的请求的 Cookie 中 根据 sessionid 取值， 取到 session_value
* 根据特殊字符串找到对应的 Session 数据 --> {'is_login': 1, 'name': 'xiaoming', 'age': 18}
* request.session.get("is_login") --> 从 Session 取值

#### Django 默认的 Session + Cookie 的登陆机制：
* 浏览器发送登陆请求 至 Django 服务
* Django 服务接收到 浏览器发送过来的请求之后，则创建 CSRFToken 以及 相关用户信息，存储到 Session 中，并且返回浏览器 Set-Cookie 的信息，通知浏览器设置相关 Cookie
* 浏览器再次发送请求 至 Django 服务，则会携带前面设置的 Cookie 信息
* Django 服务接收到 浏览器发送过来的请求之后，发现携带了 CSRFToken 以及 记录用户信息的 sessionID，根据 sessionID 查询服务器上的 session 数据。

#### Django中的Session配置
* 仅用原生django的情况
```
# Django中默认支持Session，其内部提供了5种类型的Session供开发者使用。
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串（默认）
SESSION_COOKIE_NAME = 'sessionid'
# Session的cookie失效日期（2周）（默认）
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# Session的cookie保存的域名（默认）
SESSION_COOKIE_DOMAIN = None
# 是否Https传输cookie（默认）
SESSION_COOKIE_SECURE = False
# Session的cookie保存的路径（默认）
SESSION_COOKIE_PATH = '/'
# 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_HTTPONLY = True
# 是否每次请求都保存Session，默认修改之后才保存（默认）
SESSION_SAVE_EVERY_REQUEST = False
# 是否关闭浏览器使得Session过期（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# 存储session数据默认使用的模块
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# session数据的序列化类
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
```
* 使用restframework框架编写接口
```
# restframework写的接口在上面配置的情况下会出现request.session无法设置session的问题，需要添加：
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )}
# 才能正常使用，但这只解决了单个接口的session设置
# 仍会出现一个接口设置了session，另一个接口拿不到的情况，这是由于前后端分离/跨域的情况会像是新的一台主机访问我的服务器，就会造成session的新建
# 前端解决办法，在main.ts/main.js的axios设置加上一条
axios.defaults.withCredentials = true;
```

#### Django 中设置 Session
* 与 Cookie 不同，Session设置与获取可直接操作request
* 操作方法：
  * 设置session：
    * request.session[key] = value
    * request.session.setdefault(key, value)  # 如果键已存在，不设置；否则创建并设置默认值value
  * 设置session的过期时间：
    * request.session.set_expiry(value):
    * 如果value是个整数，session会在些秒数后失效
    * 如果value是个datatime或timedelta，session就会在这个时间后失效
    * 如果value是0,用户关闭浏览器session就会失效
    * 如果value是None,session会依赖全局session失效策略
  * 获取session：request.session.get(key, default)
  * 删除指定键值对： del request.session[key]
  * 删除所有session： request.session.delete()
  * 清除session和cookie： request.session.flush()
  * 将所有session失效日期小于当前日期的数据删除： request.session.clear_expired()
  * 获取所有键： request.session.keys()
  * 获取所有值： request.session.values()
  * 获取所有键值对： request.session.items()
  * request.session.iterkeys()
  * request.session.itervalues()
  * request.session.iteritems()
  * 会话session的key： request.session.session_key
  * 检查会话session的key在数据库中是否存在： request.session.exists("session_key")

#### request库的应用
* 发出一个post请求有两种方式:request.post()和request.Session.post()
  * request.post()在调用完成后，即关闭连接，不保存cookies
  * Session.post() 调用后，保持会话连接，保存cookies
* 利用Session.post()能够实现在一个session实例发送的所有请求之间保持cookie。在向同一个主机发送多个请求时，底层的TCP连接将会被重用，显著提升性能
