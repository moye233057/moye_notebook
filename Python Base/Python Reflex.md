#### 概念
* 核心就是利用字符串去已存在的模块中找到指定的属性或方法，找到方法后自动执行——基于字符串的事件驱动
* 反射机制是很多框架的基石

#### 熟悉面向对象的属性方法
* hasattr(object,'attrName')：判断该对象是否有指定名字的属性或方法，返回值是bool类型
* setattr(object,'attrName',value)：给指定的对象添加属性以及属性值
* getattr(object,'attrName')：获取对象指定名称的属性或方法，返回值是str类型
* delattr(object,'attrName')：删除对象指定名称的属性或方法值，无返回
* getattr,hasattr,setattr,delattr对模块的修改都在内存中进行，并不会影响文件中真实内容

#### 面向对象的反射机制
* 需求描述1
  * 用户通过输入字符串来调用对象的对应方法，通过模拟一个服务器响应用户的请求，设置有注册页、登录页、主页、关于页以及错误页
  * 反射应用代码
  ```
  class WebSite:
    def register(self):
        print("欢迎来到注册页面")
    
    def login(self):
        print("欢迎来到登录页面")
    
    def home(self):
        print("欢迎进入主页")
        
    def about(self):
        print("关于我们")
        
    def error(self):
        print("404 No Found!")

  page = WebSite()        
  while True:
      choose = input("请输入你要进入的页面>>>")
      # Python面向对象中的反射：通过字符串的形式操作对象相关的属性
      # 反射机制实现上述功能，优化代码结构
      if hasattr(page,choose):
          f = getattr(page,choose)
      else:
          page.error()
  ```

* 需求描述2：
  * 输入多层的模块路径，自动生成对象并调用该类的方法。比如：notify.email.Email，notify包下面有模块email，模块email中包括了Email类，利用该类声明对象，并调用其中的send()方法。
  * 代码
  ```
  import importlib
  #'notify.email.Email'
  path_str = input("请输入包-模块-类的字符串路径：")
  module_path,class_name = path_str.rsplit('.',maxsplit=1)
  # 1 利用字符串导入模块
  module = importlib.import_module(module_path)  # from notify import email
  # 2 利用反射获取类名
  cls = getattr(module,class_name)  # Email、QQ、Wechat
  # 3 生成类的对象
  obj = cls()
  # 4 直接调用send方法
  obj.send()
  ```
