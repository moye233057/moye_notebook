实用命令
* 列出项目的树结构：  tree 项目文件夹名

一、创建
* 建立django项目：django-admin startproject 项目名称
  * manage.py：django项目管理子命令
  * 项目同名文件夹
    * __init__：Python包的初始化文件
    * wsgi.py：WEB服务网关的配置文件 - Django正式启动时，需要用到
    * urls.py：项目的主路由配置 - HTTP请求进入Django时，优先调用该文件
    * settings.py：项目的配置文件 - 包含项目启动时需要的配置
* 建立django项目App：python manage.py startapp App名称
* 创建超级管理员：python manage.py createsuperuser

二、迁移
* 建立迁移文件：python manage.py makemigrations
* 迁移（创建表）：python manage.py migrate

三、启动服务
* 命令
  * python manage.py runserver ip:port
  * 安装了uwsgi且配置好了uwsgi.ini文件后：screen uwsgi --ini uwsgi.ini
* 常见错误
  * Erro:That port is already in use
    * 原因：Django的默认启动端口已被使用
    * 解决：关闭正在运行的Django服务，重启服务

四、关闭
1. 手动操作 
  * linux终端项目运行界面按键盘ctrl+c
2. 命令行关闭
  * 知道项目运行在哪个端口，例如8000
  * lsof -i:8000
  * 找到Listen（监听）状态的那行，记录它的PID
  * sudo kill -9 PID
3. 一次性关闭所有
  * 用python manage.py runserver 0.0.0.0:8000开启的项目
  * ps -ef|grep python 能看到运行的项目是其中之一
  * 用pkill -f python -9 能够关闭所有python启动的项目