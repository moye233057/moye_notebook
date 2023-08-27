### 用过哪些
* sorted
* dict/list/set/tuple

### 常用的
数据结构/算法    语言内置                    内置库
线性结构         list（列表）/tuple(元组)    array(数组，不常用)/collections.namedtuple
链式结构                                    collections.deque(双端队列)
字典结构         dict（字典）                collections.Counter(计数器)/OrderedDict(有序字典)
集合结构         set(集合)/forzenset(不可变集合)
排序算法         sorted
二分算法                                    bisect模块
堆算法                                      heapq模块
缓存算法                                    functools.lru_cache(Least Recent Used, python3) 

### collections模块

#### 字典型
* 顺序字典：OrderedDict()
  * 记录key插入的顺序
  * 实现LRUcache
    * Least-Recently-Used 替换掉最近最少使用的对象
    * 当缓存空间不够用的时候需要一种方式剔除key
    * LRU通过使用一个循环双端队列不断把最新访问的key放到表头实现
    * 如何实现：
      * 字典用来缓存，循环双链表用来记录访问顺序
      * 利用Python内置的dict + collections.OrderedDict实现
      * dict用来当作k/v键值对的缓存
      * OrderedDict用来实现更新最近访问的key
* 缺省字典：defaultdict()
  * 带有默认值的字典
  * 即使dic['a']中'a'这个键不存在，也不会报错，而是返回一个0，可以用来实现计数器
* 链式映射：ChainMap
  * 用于管理多个词典作为单个的有效工具
  * 场景：当有多个字典表示不同的范围或上下文并且需要设置对底层数据的访问优先级时
  * 注意：
    * ChainMap支持与常规字典相同的 API，用于访问现有密钥
    * 键查找搜索目标链映射中的所有映射，直到找到所需的键。如果密钥不存在，那么将获得通常的KeyError
    * 当访问、修改、更新、删除重复键时，链映射仅会影响该键的第一个出现的键
  * 例如：
  ```
  # 可以通过.maps来修改其他映射的内容
  from collections import ChainMap

  a = {"x": 1, "z": 3}
  b = {"y": 2, "z": 4}
  c = ChainMap(a, b)
  print(c.maps)
  del c.maps[1]['z']
  print(c.maps)
  

  """
  假设您正在开发一个命令行界面 (CLI)应用程序。该应用程序允许用户指定用于连接到 Internet 的代理服务。设置优先级  
  是：

  命令行选项 ( --proxy, -p)
  用户主目录中的本地配置文件
  系统范围的代理配置
  如果用户在命令行提供代理，则应用程序必须使用该代理。否则，应用程序应使用下一个配置对象中提供的代理，依此类推。这 
  是最常见的用例之一ChainMap。
  """
  from collections import ChainMap

  cmd_proxy = {}  # The user doesn't provide a proxy
  local_proxy = {"proxy": "proxy.local.com"}
  system_proxy = {"proxy": "proxy.global.com"}

  config = ChainMap(cmd_proxy, local_proxy, system_proxy)
  config["proxy"]
  ```

#### 数组型
* 非collection模块中的数组型数据结构
  * str是字符数组，3.x使用str对象将文本数据存储为Unicode字符的不可变序列。这意味着 str型字符串数组是不可变的字符数组
  * list、tuple也属于数组型数据结构，只是一个是可变的，一个是不可变的。数组都有一个下标，且是连续分配内存的
  * array。Python里面有一个array模块，可以创建跟C语言很类似的数组，array.array用法跟list很像，唯一的区别在于 
  它只能存储同样地数据类型的数据。它所占的存储空间的大小就是数据的大小
* 基本类封装：当数据结构比较复杂时，可以构造类来封装自己的数据结构
* 命名元组：namedtuple()  让tuple属性可读
  ```
  import collections
  Point collections.namedtuple('Point', 'x, y')
  p = Point(1, 2)
  print(p.x)
  print(p.y)
  print(p[0])
  print(p[1])
  ```
* 序列化的C结构：struct，python使用struct模块执行Python值和C结构体之间的转换

#### 堆栈
* 栈是一个非常重要的数据结构，支持快速后进/先出（LIFO）语义插入和删除
* 与列表或数组不同，堆栈通常不允许随机访问它们包含的对象。插入和删除操作通常也称为push和pop
* 双向队列：deque() 
  * Python的deque对象以双向链接列表的形式实现，它的操作很像list同时，相比于list实现的队列，deque实现 
  拥有更低的时间和空间复杂度。
  * list实现在出队（pop）和插入（insert）时的空间复杂度大约为O(n)，deque在出队（pop）和入队（append 
  时的时间复杂度是O(1)
  * 当我们处理大量的数据请求的时候，比如我们需要爬大量的网站的网址，有的时候我们会将待处理的请求扔到队 
  列queue里面，用多进程或者多线程进行并发处理。比如典型的生产者消费者的模式中就经常用到queue
  ```
  import collections
  de = collections.deque()
  de.append(1)
  de.appendleft(0)
  de.pop()
  de.popleft()
  ```
* 计数器：Counter()
  * 计算可hash的对象
  * 用法：
    * Counter(dict)
      * 计数并返回一个字典，键为元素，值为元素个数
    * Counter.elements()
      * 返回一个迭代器，每个元素重复的次数为它的数目，顺序是任意的顺序
      * 如果一个元素的数目少于1，那么elements()就会忽略它
    * Counter.most_common()
      * 返回一个列表，包含counter中n个最大数目的元素，如果忽略n或者为None，most_common()将会返回 
        counter中的所有元素
      * 元素有着相同数目的将会选择出现早的元素
    * Counter.update():从一个可迭代对象（可迭代对象是一个元素序列，而非(key,value)对构成的序列）中或者另一个映射（或counter）中所有元素相加，是数目相加而非替换它们
    * subtract():从一个可迭代对象中或者另一个映射（或counter）中，元素相减，是数目相减而不是替换它们


### 集合
* set
  * 用来去掉重复元素，多个集合可以进行运算处理
* frozenset
  * 不可变集合
  * frozenset类实现的不可变set.frozenset对象是静态的，并且仅允许对其元素进行查询操作，而不能进行插入 
  或删除操作
* 多集
  * Python标准库中的collection里面的Counter类实现了一种多集或袋类型，这个类型允许集合中的元素出现多 
  次
