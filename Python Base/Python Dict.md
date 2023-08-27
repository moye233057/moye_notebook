#### 概念
* dict底层使用的是哈希表
* 平均查找时间复杂度O（1）
* CPython解释器使用二次探查解决哈希冲突问题
* 问题:
  * 哈希表是如何解决冲突的：链接法、探查法（线性探查、二次探查）
  * 扩容：
#### 判断字典是否有这个值
```
问题：用if、get还是try?
d = {"a" : 0}
# if
if 'a' in d:
    x = d['a'] + 1
else:
    x = 1
# get
x = d.get('a', 0) + 1
# try
try:
    x = d['a'] + 1
except KeyError:
    x = 1
# 结论：
# try在正常运行的时候快，if在错误运行的时候快，get的语义最清晰，最易懂，代码量也越少
# 情况：
# 如果字典没有key是一个奇怪的情况用try；
# 如果字典本来就没有这个key，但是又需要一个默认值，用get；
# 如果字典有这个键和没有这个键两种情况都属于正常情况，并且两种情况的处理不相同，用if
```

#### 反转字典
```
myinfor =  {"name":"qiwsir","site":"qiwsir.github.io","lang":"python"}
# 方法一:
infor = {}
for k, v in myinfor.items():
     infor[v]=k
# 方法二:
reverseDict = dict(zip(myinfor.values(),myinfor.keys()))
```

#### 求字典值的平均值
```
js = {"zhangsan": 90, "lisi": 78, "wangermazi": 39}
lst = sum(list(js.values())) / len(js)
print(lst)
```

#### 字典值的排序，利用sorted函数
```
js = {"zhangsan": 90, "lisi": 78, "wangermazi": 39}
# 方法一:
# 字典排序，reverse=False代表逆序
sor1 = sorted(js.items(), key=lambda x: x[1], reverse=False)
print(sor1)
# [('wangermazi', 39), ('lisi', 78), ('zhangsan', 90)]
# 方法二:
turJson = [(js[i], i) for i in js]
sor2 = sorted(turJson, reverse=False)
print(sor2)
```

#### 利用字典统计可迭代对象的数量
```
lst = [1, 2, 3, 4, 5, 1, 1, 5, 3, 5, 2, 4]
count = {}
for num in lst:
    count[num] = count.get(num, 0) + 1
print(count)
```

#### 两个字典相同键的值相减
```
# 例: 统计2022年出现，但2021年未出现的字母及其新增的次数
from collections import Counter
dic = {
    "2022": {"a": 3, "b": 2, "c": 2, "d": 2, "e": 3},
    "2021": {"a": 3, "b": 2, "c": 3, "d": 1, "f": 1},
}

res = dict(Counter(dic["2022"]) - Counter(dic["2021"]))
print(res)
# {'d': 1, 'e': 3}
```

#### 保留指定唯一数据
```
"
例: 全部数据保存在total.txt中，只需要其中与data.txt文件第一行id完全相同的数据
1  张三  男  19
2  李四  女  20
3  王五  男  34
"
import codecs
lines = codecs.open("data.txt", "r", "utf_8_sig").readlines()
dic = {}
for line in lines:
    data = line.split("  ")
    uid = data[0]
    other = " ".join(line[1:])
    dic.setdefault(uid, other)
# 有了id字典后，就可以根据id快速查找重复
uid = 4
ifuid = dic.get(uid)
if not ifuid:
    print("不符合")
else:
    del dic[uid]
```

#### 设置权重提高某个键的出现概率
```
# 应用场景
# 抽奖: 从10个人随机抽出1个有奖的, 按随机分配, 每个人的概率都是十分之一, 但是否可以在代码层面, 让某个人的概率更高些呢?
import random
# 根据值作为权重随机取数，权重为0的不会被取到，因此关键是值大于0且让想出现概率高的键权重大
a = {"张三": 0, "李四":1, "王五":0, "赵七": 0, "钱八": 0} 
r1 = random.choices(list(a.keys()), weights=list(a.values()), k=5)  # 无论取多少次都是李四
b = = {"张三": 2, "李四":1, "王五":3, "赵七": 1, "钱八": 4}
r2 random.choices(list(a.keys()), weights=list(a.values()), k=5)
print(r1)
print(r2)
```