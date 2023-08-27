#### 安装依赖
```
pip install aliyun-python-sdk-core==2.13.36
pip install aliyun-python-sdk-dysmsapi==2.1.2
pip install Aliyunsdkcore==1.0.3
```

#### 发送短信方法
```
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

def send_sms(to_phone, param, TemplateCode,
             AccessKeyId='',
             AccessKeySecret='',
             SignName='',
             RegionId='',
             ):
    """
    发送短信
    :param to_phone: 接收人
    :param param: 替换参数
    :param TemplateCode:  模板CODE
    :param AccessKeyId: 自己的 AccessKeyId
    :param AccessKeySecret: 自己的 AccessKeySecret
    :param RegionId:    地址（默认的就行）
    :param SignName:    签名名称（在签名管理里面）
    :return:
    """
    credentials = AccessKeyCredential(AccessKeyId, AccessKeySecret)
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    client = AcsClient(region_id='cn-hangzhou', credential=credentials)

    request = SendSmsRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId', RegionId)
    request.add_query_param('PhoneNumbers', to_phone)
    request.add_query_param('SignName', SignName)  # 注意必须是审核通过的
    request.add_query_param('TemplateCode', TemplateCode)  # 注意必须是审核通过的
    # 变量名指的是阿里云短信服务，创建短信模板时添加的动态变量${name}中的name
    # 替代短信模板中的变量！！！param的格式为：{"变量名1":"值1","变量名2":"值2",...}
    request.add_query_param('TemplateParam', param)
    response = client.do_action_with_exception(request)
    return response
```

#### 实战
```
send_sms(submitphone, {'name': name, 'content': content}, TemplateCode='SMS_242575902')
```