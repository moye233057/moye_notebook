#### 微信小程序官方登录(获取openid)
* 官方文档地址：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
* 请求方式：GET
* 请求url：'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'
  * 四个参数：appid、secret、js_code、grant_type
  * appid： 在“微信开发平台”中的开发-开发管理-开发设置中能直接看到
  * secret： 在“微信开发平台”中的开发-开发管理-开发设置中生成
  * js_code： 需要小程序前端用wx.login方法生成，传递给后端
  * grant_type： 授权类型，是一个固定值，authorization_code
* 最简单的请求流程：
```
code = request.POST.get('code')  # 前端传递
appid = ""
appsecret = ""
code_url = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(appid, appsecret, code)
response = requests.get(code_url)
json_response = response.json()  # 把它变成json的字典
if json_response.get("session_key"):
    print(json_response)
else:
    print('error')
```
* 生产环境使用的配置：
  * settings.py
  ```
  AppId = ''  # 写自己的小程序id
  AppSecret = ''  # 写自己小程序的密钥
  code2Session = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'  # 需要获取微信小程序code
  ```
  * models.py
  ```
  class Wxuser(models.Model):
      id = models.AutoField(primary_key=True)
      openid = models.CharField(max_length=255, )
      name = models.CharField(max_length=50, verbose_name="昵称")
      avatar = models.CharField(max_length=200, verbose_name="头像url")
      phone = models.CharField(max_length=20, verbose_name="电话")
      countryCode = models.CharField(max_length=8, verbose_name="电话区号", default='', blank=True, null=True)
      creat_time = models.DateTimeField(auto_now_add=True, verbose_name="第一次登录时间")
  ```
  * views.py
  ```
  from project import settings
  from django.http import JsonResponse
  from django.core.cache import cache

  def get_user_info(code, appid=settings.AppId, appsecret=settings.AppSecret):
      """通过小程序前端传来的code,后端向微信官方后台发送请求,获取微信用户的openid和session_key"""
      code_url = settings.code2Session.format(appid, appsecret, code)
      response = requests.get(code_url)
      json_response = response.json()  # 把它变成json的字典
      # print(json_response)
      if json_response.get("session_key"):
          return json_response
      else:
          return False

  def wx_login(request):
      """
      作用：前端与后端交互的微信登录
      备注：新版微信不给开发者直接获取用户隐私信息，如果需要用户的昵称与头像可以让用户自行上传
      """
      code = request.POST.get('code')
      if not code:
          return JsonResponse({'code': 404, "msg": "缺少参数"})
      else:
          appid = settings.AppId
          user_data = wx_login(code, appid)  # 用appid和code获取用户基本信息
          if user_data:
              # 将session_key进行md5加密，作为缓存的键
              md5 = hashlib.md5()
              md5.update(str(time.clock()).encode())
              md5.update(user_data['session_key'].encode('utf-8'))
              token = md5.hexdigest()

              # 查看用户是否已登录，如果没有登录，创建基本信息记录
              has_user = Wxuser.objects.filter(openid=user_data['openid']).first()
              if not has_user:
                  has_user = Wxuser.objects.create(openid=user_data['openid'])
              
              # 将登录信息记入缓存中 
              val = user_data['session_key'] + "&" + user_data['openid']
              cache.set(token, val, timeout=60 * 60 * 24 * 30)

              return JsonResponse({
                    'code': 200,
                    'msg': 'ok',
                    'data': {
                        'token': token,
                        'openid': user_data['openid'],
                    }
                })
          else:
              return JsonResponse({'code': 404, 'msg': '无效的code', 'data': None})  
  ```

#### 微信小程序获取用户手机号的方法
* 第一步：获取稳定版接口调用凭据
  * 官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getStableAccessToken.html
  * 请求方式：POST
  * 请求url：https://api.weixin.qq.com/cgi-bin/token
  * 请求参数：
    * grant_type : 固定值client_credential （有坑，看官方文档很容易误解为需要其它接口来获取这个参数，但其实是一个固定值）
    * appid：小程序id
    * secret：小程序密钥
  * 请求代码：
  ```
  acess_token_url = "https://api.weixin.qq.com/cgi-bin/token"
  data1 = {
      "grant_type": "client_credential",
      "appid": "",  # 填自己的appid
      "secret": "",  # 填自己的app密钥
  }
  res = requests.post(acess_token_url, data1)
  res = json.loads(res.text)
  access_token = res["access_token"]  # 接口调用凭证
  ```

* 第二步：用接口调用凭证和**前端传来的手机号获取凭证**获取手机号
  * 官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
  * 请求方式：POST
  * 请求url："https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={}".format(access_token)
    * 注意：有坑，文档中的acess_token是要拼接在url中的，而不是放在请求体中
  * 请求参数：
    * code： 手机号获取凭证 （有坑，这个code和微信登录wx.login获取的code是不一样的，需要小程序前端用button组件和相应的方法获取）
    * 小程序前端手机号获取凭证的获取参考：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html
  * 请求代码：
  ```
  phone_url = "https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={}".format(access_token)
  # 有坑，用requests请求的写法如下，用data = {}的格式可能会出错
  res = requests.post(phone_url, data=json.dumps({'code': phone_code}), headers={'Content-Type': 'application/json'})
  res = json.loads(res.text)
  phone = res["phone_info"]["purePhoneNumber"]  # 手机号
  countryCode = res["phone_info"]["countryCode"]  # 区号，其他返回值见官方文档
  ```
