### urllib
* quote() 将单个字符串编码转化为 %xx 的形式
```
from urllib.parse import quote
# 例1：url标准符号：数字字母
KEYWORD = 'ipad'
url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
print(url)
# 运行结果：https://s.taobao.com/search?q=ipad
KEYWORD = '3346778'
url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
print(url)
# 运行结果：https://s.taobao.com/search?q=3346778

# 例2：特殊符号：汉字、&、=等特殊符号编码为%xx
from urllib.parse import quote
"""特殊符号：汉字、&、=等特殊符号编码为%xx """
KEYWORD = '苹果'
url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
print(url)
# 运行结果：https://s.taobao.com/search?q=%E8%8B%B9%E6%9E%9C
KEYWORD = '='
url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
print(url)
# 运行结果：https://s.taobao.com/search?q=%3D

# 例3：指定其它编码
from urllib.parse import quote
text = quote("药品互联网信息服务", encoding="gb2312")
print(text)
# 运行结果：%D2%A9%C6%B7%BB%A5%C1%AA%CD%F8%D0%C5%CF%A2%B7%FE%CE%F1

```