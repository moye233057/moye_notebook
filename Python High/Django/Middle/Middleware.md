* 中间件类须继承自 django.utils.deprecation.MiddlewareMixin类
* 中间件类须实现下列五个方法种的一个或多个：
  * process_request(self, request)
    * 调用位置： 执行路由之前被调用，在每个请求上调用，返回None或HttpResponse对象
    * 应用场景：
      * 请求的过滤：ip地址黑白名单
      * 登录信息记录
  * process_view(self, request, callback, callback_args, callback_kwargs)：
    * 调用位置：调用视图函数之前
    * 参数说明：callback当前请求路由对应的视图函数，callback_args视图函数的位置传参，callback_kwargs视图函数的关键字传参
    * 调用视图之前被调用，在每个请求上调用，返回None或HttpResponse对象
    * 应用场景：
      * 记录调用了哪些视图函数
      * 替换视图函数的参数
  * process_response(self, request, response)
    * 调用位置：响应返回浏览器前被调用，在每个请求上调用，返回HttpResponse对象
  * process_exception(self, request, exception) 
    * 当处理过程中抛出异常时调用，返回一个HttpResponse对象
  * process_template_response(self, request, response)
    * 调用位置：在视图函数执行完毕且视图返回的对象中包含render方法时被调用；该方法需要返回实现了render方法的响应对象
  * 中间件中大多数方法在返回Nond时表示忽略当前操作进入下一项事件，当返回HttpResponse对象时表示此请求结束，直接返回给客户端