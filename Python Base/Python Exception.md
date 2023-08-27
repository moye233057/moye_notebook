#### 参考资料
* 关于Django中，raise的使用
https://www.cnblogs.com/geshuying/p/14972998.html

#### 异常等级
BaseException
-- SystemExit
-- KeyboardInterrupt
-- GeneratorExit
-- Exception
   -- ...

#### 异常使用的场景
* 网络请求（超时、连接错误等）
* 资源访问（权限问题、资源不存在）
* 代码逻辑（越界访问、KeyError等）

#### 处理Python异常
```
try:
    # func    # 可能会抛出异常的代码
except (Exc1, Exc2) as e:  # 可以捕获多个异常并处理
    # 异常处理的代码
else:
    # pass   # 异常没有发生的时候的代码逻辑
finally:
    pass    # 无论异常有没有发生都会执行的代码
```

#### 如何自定义自己的异常？为什么要定义自己的异常？
* 继承Excepion实现自定义异常
  * 为什么不是BaseException?(使用BaseException能用crtl+C结束这个程序吗？)
* 给异常加上一些附加信息
* 处理一些业务相关的特定异常（raise MyException）