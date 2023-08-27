### 一、类
* #### 类属性
  定义在类里面，类中方法之外的变量，被该类的所有对象所共享
* #### 类方法
  由@classmethod装饰的方法,能够使用类名直接访问
  第一个参数必须要默认传类，一般习惯称为cls。
  ```
  @classmethod
  def class_method(cls):
      pass
  ```
  **静态方法和类方法既可以通过实例调用，也可以通过类来调用，而一般方法必须用通过绑定实例调用。**
* #### 实例属性
  实例变量指的是在任意类方法内部，以“self.变量名”的方式定义的变量
  特点：
  1. 只作用于调用方法的对象
  2. 实例变量只能通过对象名访问，无法通过类名访问。
* #### 实例方法
  1. 写在类里面，没有任何装饰的方法，第一个参数必须要默认传实例对象，一般习惯用self。反过来，一个类的方法里面带有self参数，就可以称为实例方法
  2. 实例（绑定）方法只能被实例对象调用，通过实例.方法名()来调用(Python3 中，如果类调用实例方法，需要显示的传self, 也就是实例对象自己)，调用的时候在方法后面要跟括号（括号中默认有self参数，但是不写出来），通过实例调用方法，我们称这个方法  绑定在实例上。
  3.调用非绑定方法，例如super调用被重写的父类方法
  ```
  class A:
      def ShiLi_method(self):
          pass 
  ```
* #### 静态方法
  由@staticmethod装饰的方法，能够使用类名直接访问
  对参数没有要求
  ```
  @staticmethod
  def static_method():
      pass
  ```

* #### 初始化方法
  ```
  class A:
      def __init__(self, name):
          self.name = name  # self.name称为实体属性，用赋值操作将局部变量name的值赋给了实体属性
  ```

* #### 实例动态绑定属性和方法。
  类的实例可以再次绑定属性和方法
  例如：
  ```
  class Student:
      def __init__(self, name, age):
          self.name = name
          self.age = age
  stu1 = Student('张三', 15)
  stu2 = Student('李四', 16)
  # 这样stu1和stu2都有各自的实例属性name和age
  # 如果加入：
  stu1.agent = '男'
  # stu1就多了一个属性agent
  # 如果加入：
  def show():
      print('我是一个函数')
  stu1.show = show
  # stu1就多了一个方法
  ```

* #### 总结
  1.实例方法用的最多
  2.类方法可以返回这个类的实例
  3.静态方法可以不用返回任何实例属性与类的实例

  类的理解:
  1. 一个类被实例化，这个实例会拥有这个类的类属性，此时**修改类的类属性，实例的这个属性（类属性）**也会变化
  2. 当这个**实例的‘类属性’被修改**之后，会重新创建一个实例变量，而不会对类变量进行修改，此时实例拥有了**与类变量同名的实例变量**。
  3. 修改类属性不会改变实例属性，修改实例属性也不会改变类属性。
  4. 如果删除一个实例的与类属性同名的实例属性，该同名属性又会变为类属性，受类属性修改而变化
  5. 在类确定或者实例化之后，也可以增加和修改(实例)属性，其方法就是通过类或者实例的点号操作来实现，即object.attribute，可以实现对属性的修改和增加。
  6. 同时存在同名的类变量和实例变量时，实例.变量名只会查找到实例变量，这是因为实例会先从__init__中查找变量
  7. 类属性可以共享于多个实例对象
  8. 多继承中类属性与实例属性及方法的调用顺序:
     不同的继承关系会调用不同的搜索方式（c3算法）
     查看类属性/方法的调用顺序:print(class.__orm__)

* #### 抽象基类
  尽量少用，如果技术不够会导致约束限制不符合编程逻辑
  """
  场景一
  抽象基类不能实例化
  继承抽象基类必须重载内部方法
  """
  ```
  s = Sized()
  class Test(Sized):
      def __len__(self):
          pass
  ```
  """
  场景二
  实现某个类的时候，必须实现指定的方法
  框架中比较多，例如django的缓存功能，redis/cache/memorycache，用户使用哪一种是不确定的，因此这三种需要在方法调用上统一
  因为不确定用户使用的是redis缓存还是文件缓存，两种缓存不一样，必须让用户自己实现
  """
  ```
  #需要一个缓存基础类CacheBase
  #如果用户没有重新set(设置缓存)和get(获取缓存)方法，抛出异常
  #这样设置在继承的时候不会出现，但是在调用方法的时候会抛出异常
  class CacheBase:
      def get(self):
          raise NotImplementedError
    
      def set(self):
          raise NotImplementedError
  #这时候可以用抽象基类来实现上述功能
  import abc
  class CacheBase:
      @abc.abstractmethod
      def get(self):
          pass
      @abc.abstractmethod
      def set(self):
          pass
  #这样继承类的时候如果没有实现对应抽象方法，会提示
  ```

* #### 私有属性
  私有属性无法被实例对象直接获取
  在继承关系的子类也无法直接获取到私有属性
  私有属性只能被当前这个类的方法获取
  在python中，私有属性其实是python在执行过程中对私有属性的名称进行了重命名
  _类名.__属性名称

* #### 多继承
    mixin模式
    特点
    1.mixin模式功能单一(比如只有一个方法)
    2.不和基类关联，可以和任意基类组合，基类可以不和mixin关联就能初始化成功
    3.不使用super方法

### 二、应用
静态方法与类方法返回类对象时的区别:
```
"""
静态方法调用:类.方法名
类方法调用:类.方法名
区别在于类方法需要传入一个cls参数，这个参数指向类本身
"""
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        reaturn F"{self.year}/{self.month}/{self.day}"

    @staticmethod
    def parse_from_string(date_str):
        #静态方法返回类的时候时写上当前的类名，硬编码，如果类名更改，那么返回的类名也必须保持一致
        year, month, day = tuple(date_str.split("-"))
        return Date(int(year), int(month), int(day))
    
    @classmethod
    def parse_from_string(cls, date_str):
        #cls参数指向当前这个类，不能与实例搞混
        year, month, day = tuple(date_str.split("-"))
        return cls(int(year), int(month), int(day))
```


三、继承
* 当一个类继承自另一个类，它就被称为一个子类/派生类，继承自父类/基类/超类。它会继承/获取所有类成员（属性和方法）
* Python支持如下种类的继承：
  * 单继承：一个类继承自单个基类
  * 多继承：一个类继承自多个基类
  * 多级继承：一个类继承自单个基类，后者则继承自另一个基类
  * 分层继承：多个类继承自单个基类
  * 混合继承：两种或多种类型继承的混合