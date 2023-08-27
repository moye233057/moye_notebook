#### 参考资料
* @property的介绍与使用
https://zhuanlan.zhihu.com/p/64487092

#### 概念
* 装饰器是在一个函数的前后去执行代码
* 装饰器是将被装饰和函数作为参数传递到装饰器（函数）中执行
* 装饰器类似数学中的复合函数，在函数上面再套一个函数，也就是y = g(f(x)) 
* 装饰器本质是一个闭包函数
  * 闭包偏向于利用内存常驻的特点，而装饰器偏向于利用函数返回函数的特点
  * 闭包函数是函数的嵌套，函数内还有函数，即外层函数嵌套一个内层函数
  * 在外层函数定义局部变量，在内层函数通过nonlocal引用，并实现指定功能，比如计数，最后外层函数return内层函数
  * 主要作用：可以变相实现私有变量的功能，即用内层函数访问外层函数内的变量，并让外层函数内的变量常驻内存
  * 闭包函数实现计数器功能
  ```
  #外层函数
  def outter_func():
      #定义外层函数的局部变量
      a=0
      #定义一个内层函数
      def inner_func():
          #声明下在内层函数内，a变量指向到外层函数的a
          nonlocal a
          a+=1
          print(a)
      #返回内层函数
      return inner_func
 
  counter=outter_func()
  counter() #输出为1
  counter() #输出为2
  ```

#### 装饰器类型
* 不带参数的装饰器（本质是两层函数的嵌套）
```
# @wraps的作用：接受一个函数来进行装饰，并加入了复制函数名称、注释文档、参数列表等等的功能。这可以让我们在装饰器里面访问在装饰之前的函数的属性
def decorator_name(f):
    # @wraps(f)
    def decorated(*args, **kwargs):
        """这是装饰的描述"""
        if not can_run:
            return "Function will not run"
        return f(*args, **kwargs)

    return decorated


@decorator_name
def func():
    """这是func的描述"""
    return ("Function is running")


can_run = True
print(func())
print(func.__name__)
print(func.__doc__)
# 假如没有@wraps，打印的是wrapTheFuction；加上@wraps，打印的是be_decorator
# 原理： @wraps能复制被装饰的函数func的信息给decorated
```
* 带参数的装饰器
```
# 带参数装饰器，即可以向装饰器传参，以为装饰器赋予个性化定制的特点，根据传入参数不同，装饰器表现行为不同等等
# 此时，需要再加一层函数嵌套，最外层函数主要实现传参的功能，然后返回第二层函数，此时就又退化成了两层嵌套，即不带参装饰器
# @deco(a=1)在调用@之前会首先执行deco(a=1)得到一个实际的装饰器, 带参数的装饰器deco(a=1)模块导入时立即执行

from functools import wraps
def dec_with_args(*args):
    def dec(func):
        @wraps(func)
        def in_dec(*args):
            """
            your decorator code
            """
            return func(*args)
        return in_dec
    return dec
 
@dec_with_args((*args)
#此处，可以认为先调用了一次外层函数，返回了dec函数，然后再将myfunc函数传给dec函数
#1、dec_with_args(*args)返回dec函数
#2、此时，变为@dec，等同于myfunc=dec(myfunc)，又回到了不带参的装饰器
def myfunc():
    pass
```

* 类装饰器
```
类也可以用来构建装饰器
例子1：
from functools import wraps 
#定义一个装饰器名称的类
class  with_para_decorator: 
    #在类的__init__函数内接受装饰器参数，并赋值给类的实例参数，这样可以让其他函数随时使用
    #当然，如果装饰器没有参数，此处不转a,b即可，相当于类无参实例化
	def __init__(self,a,b):    
	    self.a=a	
	    self.b=b	
    #在类的__call__函数内接受被装饰函数，并具体定义装饰器
	def __call__(self,func):   
	    @wraps(func)   			
	    def wrap_function(arg1,arg2):  
		print('装饰带参数的函数，函数传的参数为：{0}, {1}'.format(arg1,arg2))
		print('带参数的装饰器，装饰器传的参数为：{0}, {1}'.format(self.a,self.b))
		return func(arg1,arg2)   
	return wrap_function
 
#使用装饰器
@with_para_decorator(1,2)  
def need_decorate(a,b):   
    pass
need_decorate(4,5)		   
```

* 装饰器实现动态属性
form datetime import datetime
class User:
    def __init__(name, birthday):
        self.name = name
        self.birthday = birthday
        self._age = 0
    
    @property
    def age(self):
        retrun datetime.now().year - self.birthday.year
    
    @age.setter
    def age(self, value):
        self._age = value


#### 应用
* 装饰器应用的基本原则：
  * 希望为存量函数和代码增加新功能，同时又不希望对原有函数进行调整（包括代码和调用方式等）
  * 较多其他函数均需要该新增功能，希望一处实现，多处复用，提升代码可读性和可维护性
* 1、类型检查：
  * 蓝本规范:@wrap
* 2、用户验证（登录注册校验）/授权(Authorization)
  * 装饰器能有助于检查某个人是否被授权去使用一个web应用的端点(endpoint)。它们被大量使用于Flask和Django web框架中
  * 一些接口函数需要登录/注册过后才能使用
  * 注册表隔离
* 3、格式化输出
  ```
  import json
  from functools import wraps
  def json_output(func): # 将原本func返回的字典格式转为返回json字符串格式
    @wrap(func)
    def inner(*args, **kwargs):
      return json.dumps(func(*args, **kwargs))
    return inner
  ```
* 4、异常捕获
* 5、日志管理
  ```
  # 日志类1
  from functools import wraps
  class logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)
        return wrapped_function

    def notify(self):
        # logit只打日志，不做别的
        pass
  # 这个实现有一个附加优势，在于比嵌套函数的方式更加整洁，而且包裹一个函数还是使用跟以前一样的语法：
  @logit()
  def myfunc1():
      pass
  # 给logit创建子类，添加email的功能
  # 日志+发送右键类
  class email_logit(logit):
      '''
      一个logit的实现版本，可以在函数调用时发送email给管理员
      '''
      def __init__(self, email='admin@myproject.com', *args, **kwargs):
          self.email = email
          super(logit, self).__init__(*args, **kwargs)
  
      def notify(self):
          # 发送一封email到self.email
          # 这里就不做实现了
          pass
  从现在起，@email_logit将会和@logit产生同样的效果，但是在打日志的基础上，还会多发送一封邮件给管理员
  ```
  ```
  # 日志类2
  from functools import wraps
  import datetime
  #定义一个可以记录函数调用时间、传入参数的装饰器
  def dec(log_file):
      #接受log_file参数，供具体实现装饰器功能的函数使用
      def dec_print_info(func):
          @wraps(func)
          def print_info(a,b):
              #该函数，因为本身没有定义log_file变量，python此时会逐层往上找寻，找到了最外层传入的log_file变量，然后使用
              with open (log_file,'a+') as f:
                  hour=datetime.datetime.now().hour
                  minute=datetime.datetime.now().minute
                  second=datetime.datetime.now().second
                  f.write('调用时间：{}点{}分{}秒，传入的参数为：{}和{}\n'.format(hour,minute,second,a,b))
              return func(a,b)
          return print_info
      return dec_print_info
   
  #加装饰器时，传入日志文件地址
  @dec('/users/yanweichao/downloads/log2.txt')
  def myfunc(a,b):
      return a+b
  myfunc(12,59)
  ```
