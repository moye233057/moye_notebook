#### 参考资料
* Python之string模块（详细讲述string常见的所有方法）
https://www.cnblogs.com/lyy135146/p/11655105.html
* Python之re模块 
https://www.cnblogs.com/shenjianping/p/11647473.html
* Python批量模糊匹配的3种方法实例
https://www.jb51.net/article/239151.htm
* 正则表达式30分钟入门教程
https://deerchao.cn/tutorials/regex/regex.htm
* 什么是正则表达式？
https://github.com/ziishaned/learn-regex/blob/master/translations/README-cn.md

#### 判断是否包含(全是)中英文
```
# 是否全是中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

# 是否包含中文
def is_include_Chinese(text):
    if sum([1 if u'\u4e00' <= i <= u'\u9fff' else 0 for i in text]) > 0:
        return True
    else:
        return False

# 是否全是英文
def is_all_english(strs):
    import string
    for i in strs:
        if i not in string.ascii_lowercase + string.ascii_uppercase:
            return False
    return True

print(is_all_english("hello"))
print(is_all_english("hello你好"))
print(is_all_english("123456"))
print(is_all_english("你好"))

# 是否包含英文
import re
def is_contains_english(str):
    my_re = re.compile(r'[A-Za-z]', re.S)
    res = re.findall(my_re, str)
    if len(res):
        return True
    else:
        return False

print(is_contains_english("hello"))
print(is_contains_english("hello你好"))
print(is_contains_english("123456"))
print(is_contains_english("你好"))
```

#### 将字符串中所有连续重复的字符只保留一个
```
# 例如:aaacdefbbb  -> acdefb
def removeRepeat(_str):
    _list = list(_str)
    n = len(_list)
    if n <= 1:
        return
    list1 = []
    for i in range(n - 1):
        if _list[i] != _list[i + 1]:
            list1.append(_list[i])
        # 如果只对非中文生效，is_Chinese是方法一
        # else:
        #    if not is_Chinese(_list[i]):
        #        list1.append(_list[i])
    list1.append(_list[-1])
    str1 = ''.join(list1)
    return str1
```

#### 不定长连续重复字符串判断
```
# 思路: 对字符串进行分词去重操作，看不重复词的数量以及去重后新词组和原词组的比值
# 例: 
import jieba
import re
t0 = "九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读九书网提供分享阅读"
def setTextCount(text):
    subtext = re.sub(r"[a-zA-Z0-9%$#.(),?。]", "", text)
    old = list(jieba.cut_for_search(subtext))
    new = list(set(old))
    if len(new) <= 10:
        return False  # 根据剩余词数量判断
    elif len(new) / len(old) < 0.1:
        return False  # 根据词语减少的阈值判断
    else:
        return True
```

#### 字符串中中文所占的百分比
```
def percentage_Chineses(text):
    percen = sum([1 if u'\u4e00' <= i <= u'\u9fff' else 0 for i in text]) / len(text)
    return percen
```

#### 正则表达式匹配数字和字母组合，且不能为纯数字或纯字母
```
^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$
```

#### 比较两个字符串的相似度
```
from fuzzywuzzy import fuzz
t1 = "答案错7驾驶人要按照驾驶证载明的准驾车型驾驶车辆。答案对8行车中前方遇自行车影响通行时，可鸣喇叭提示，加速绕行。答案错9在大雨天行车，为避免发生水滑而造成危险，要控制速度行驶。答案对10对未取得驾驶证驾驶机动车的，追究其法律责任。答案对"
t2 = "答案错7使用其他机动车号牌行驶证的一次记3分。答案错8行车中前方遇自行车影响通行时，可鸣喇叭提示，加速绕行。答案错9驾驶人将机动车交给驾驶证被暂扣的人驾驶的，交通警察给予口头警告。答案错10对未取得驾驶证驾驶机动车的，追究其法律责任。答案对"
r1 = fuzz.ratio(t1, t2)
print(r1)
```

#### jieba判断词性
```
from jieba import posseg
s = "行车中前方遇自行车影响通行时"
pos = posseg.cut(s)
for w, flag in pos:
    print(w, flag)
```

#### 变形词检查
```
# 想检查一对字符串中，其中一个字符串是否是另一个字符串的变形词
from collections import Counter
s1 = "listen"
s2 = "lstnie"
res = Counter(s1) == Counter(s2)
print(res)
```

#### 生成四位验证码
```
import string
import random

length = 4
al = string.ascii_letters
di = string.digits
print(al, di)
li = random.sample(al + di, length)
print(li)
```

#### 判断整数、小数、百分数
```
def is_number(s):
    if s.count(".") == 1 and s[-1] != "%":  # 小数的判断
        if s[0] == "-":
            s = s[1:]
        if s[0] == ".":
            return False
        s = s.replace(".", "")
        for i in s:
            if i not in "0123456789":
                return False
        else:  # 这个else与for对应的
            return True
    elif s.count(".") == 0 and s[-1] != "%":  # 整数的判断
        if s[0] == "-":
            s = s[1:]
        for i in s:
            if i not in "0123456789":
                return False
        else:
            return True
    elif s[-1] == "%":  # 百分数判断
        return True

    else:
        return False


print(is_number("1334345345"))
print(is_number("1.12344565"))
print(is_number("-14344343"))
print(is_number("-1.123456"))
print(is_number("10%"))
print(is_number("nihao"))
print(is_number("你好"))
```
