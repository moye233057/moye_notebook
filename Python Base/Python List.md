#### 参考资料
* 删除列表中具有连续重复项的元素
https://blog.csdn.net/be_racle/article/details/124761429

#### 去除空值
```
lst = ["", "", "a", "b"]
lst = list(filter(None, lst))
print(lst)
```

#### set操作list 
```
# 不保留原始顺序的列表去重
lst = [1,1,2,2,2,3,3,3,3]
lst = list(set(lst))
# 给定两个列表，找出相同元素与不同元素
lst1 = [1, 2, 3]
lst2 = [3, 4, 5]
set1 = set(lst1)
set2 = set(lst2)
print(set1&set2)
print(set1^set2)
```

#### 列表取值
```
import random
lst =["数学", "语文", "英语", "物理", "化学", "政治", "生物", "地理", "历史"]
# 随机选择一个
res1 = random.choice(lst)
print(res1)
# 随机选择多个
res2 = random.sample(lst, 3)
print(res2)
# 判断多个词是否在某个字符串中
words = ['a', 'b', 'c', 'd']
s = "apple"
if any([w in s and w for w in words]):
    print("yes")
else:
    print("false")
# 取出路径下的所有文件夹名称
import os
src = "./"
filenames = [name for name in os.listdir(src) if os.path.isdir(name)]
print(filenames)
# 打乱一个排好序的list对象alist
import random
random.shuffle(alist)
```

#### list列表推导式
```
# 循环平方
squares = [x**2 for x in range(1,10)]
# 循环去除两边空格
mybag = [' glass',' apple','green leaf ']   #有的前面有空格，有的后面有空格
[one.strip() for one in mybag]
# 取出在列表lst1但不在lst2的元素
lst1 = ['a', 'b', 'c', 'd']
lst2 = ['a', 'e', 'f']
res = [i for i in lst1 if i not in lst2]
print(res)
# 取出以lst2内元素结尾的lst1中的元素
lst1 = ['apple', 'egg', 'python', 'list', 'dict']
lst2 = ['e', 't']
res = []
for word in lst1:
    if any([word.endswith(i) for i in lst2]):
        res.append(word)
print(res)
# 危险词去除
riskword = ["a", "b", "c"]
words = ["apple", "egg", "python"]
res = []
for word in words:
    if all([rw not in word for rw in riskword]):
        res.append(word)
print(res)
```

#### 将列表中的第一个移到最后一位。
```
lst = [0,1,2,3,4,5]
last = lst.pop(0)
lst.append(last)
```

#### 求两个列表之间的相似度(元素只有相同和不同两种情况)
```
import difflib

lst1 = [1, 1, 2, 2, 2, 3, 3, 3, 3, 8]
lst2 = [1, 1, 2, 2, 2, 3, 3, 3, 3, 7]
sm = difflib.SequenceMatcher(None, lst1, lst2)
print(sm.ratio())
```

#### 列表排序
```
# 使用lst.sort(reverse=False, key=)，注意没有返回值
# key不填默认以列表元素为排序依据，reverse=True代表从大到小排序
# 简单排序
lst = [1, 5, 9, 7, 3]
lst.sort()
# 按lst1中元素age由大到小排序
lst1 = [{'name':'a', 'age':20}, {'name':'b', 'age':30}, {'name':'c', 'age':25}]
sorted(lst1, key=lambda x:x['age'], reverse=True)
print(lst1)
# 对列表进行去重后，想将其恢复到原来的顺序
lst1 = [1, 2, 5, 7, 8, 9, 1, 3, 4, 1, 2, 1]
lst2 = lst1.copy()  # 浅拷贝，不会拷贝列表里面的元素
lst1 = list(set(lst1))
print(lst1)
lst1.sort(key=lst2.index)
print(lst1)
```

#### 列表切割
```
def cutlist(list, pagenum, neednum):
    """
    list: list.要切割的列表
    pagenum: int.当前页码/起始位置
    neednum: int.每页个数/结束位置的偏移量
    """
    listlength = len(list)
    returnlist = []
    if listlength > 0:
        leftnum = 0 + (pagenum - 1) * neednum
        rightnum = leftnum + neednum
        if leftnum < listlength < rightnum:
            returnlist = list[leftnum:listlength]
        elif listlength >= rightnum:
            returnlist = list[leftnum:rightnum]
        return returnlist, listlength
    else:
        return returnlist, listlength
```

#### 多维列表数据过滤特定条件的列表
```
# 例: 取出以字典为元素的列表中year为2022的值
year = 2022
data = [
    {
        "year": 2021,
        "word": "鼠标",
    },
    {
        "year": 2019,
        "num": "电话",
    },
    {
        "year": 2022,
        "num": "智能",
    },
    {
        "year": 2022,
        "num": "足球",
    },
    {
        "year": 2018,
        "num": "家电"
    },
]
new_data = list(filter(lambda x: x["year"] == year, data))
print(new_data)
```


#### 对列表中相同元素箱
```
# 目标: [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5] -->  [[1, 1, 1], [2, 2, 2], [3, 3], [4, 4], [5]]
from collections import Counter
box = [1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5]
# 方法一
last = box[0]
temp = [box[0]]
cutbox = [temp]

for item in box:
    if item == last:
        temp.append(item)
    else:
        last = item
        temp = [item]
        cutbox.append(temp)

# 方法二
cou = Counter(box)
cutbox = []
for key, value in dict(cou).items():
    cutbox.append([key]*value)
print(cutbox)
# 方法三
cutbox = []
for i in set(box):
    cutbox.append([i]*box.count(i))
print(cutbox)
```

#### 将列表数据分为每三个一组
```
lists= [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
n = 3 # 表示多少个一组
list = [lists[i:i+n] for i in range(0,len(lists),n)]
print(list) # [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12]]
```

#### 两个列表的全组合
```
# 方式一:
import itertools

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8,9]
print(list(itertools.product(list1, list2)))

# 方式二:
list3 = [[x,y] for x in list1 for y in list2]
print(list3)

# 方式三:
from itertools import permutations
a = [1, 2, 3]
b = [4, 5, 6]
for p in permutations(b):
    print(b)
lst = [list(zip(a, p)) for p in permutations(b)]
print(lst)
```

#### 统计列表中出现的元素个数
```
# 统计字符串中分词后各个词出现的次数
import jieba
from collections import Counter

text = "1经常保持微笑智慧泡2常运动智慧泡3保持充足的睡眠智慧泡4乐于助人智慧泡5学会和各种人愉快的相处智慧泡6保持高度的自信心智慧泡7持有童真智慧泡8充满好奇智慧泡9具有幽默感智慧泡10装酷也可以智慧泡11服装要潮流智慧泡12做到风度翩智慧泡13有自己的兴趣爱好智慧泡14勇于突破危险智慧泡15有接受意外的心态智慧泡16有创意智慧泡17知道怎样利用能源比如拖地智慧泡18一定要有追求目标智慧泡19对未来有展望智慧泡20保护弱小智慧泡21与兄弟姐妹相亲相爱智慧泡22要学会合作，创造奇迹智慧泡23再怎么艰难，都不要放弃所爱的人智慧泡24重要的东西还是不要轻易失去例如初吻智慧泡25不要总是面带色相智慧泡26千万不要得罪女朋友智慧泡27不要为失恋而茶不思，饭不想智慧泡28不要欺压别人智慧泡29不要随便惊吓朋友智慧泡30有空来家坐智慧泡31看到好贴一定要回复智慧泡32不要恶意灌水智慧泡"
text = jieba.cut_for_search(text)
res = list(text)
print(res)
print(len(res))
# 统计列表中各元素出现次数，most_conmmon获取最多的前N个，数据格式[(item, num)]
most = Counter(res).most_common(1)
most_num = most[0][1]
```

#### 对两个不同长度的列表进行迭代操作
```
a = [1,2,3,4,5]
b = ["python","www.itdiffer.com","qiwsir"]
(1)
d = []
for x, y in zip(a, b)
    d.append(x+y)
(2)
length = len(a) if len(a)<len(b) else len(b)
for i in range(length):
    c.append(str(a[i]) + ":" + b[i])
```

#### 将列表中的元素进行类型转换
```
lst = list(map(type, lst))
type可以是int、str...,取决与数组中的数据类型
```