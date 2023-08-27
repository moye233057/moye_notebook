#### 连接
```
import redis
# 通过redis对象连接
# decode_responses为True时存入的是字符串数据，False存入字节数据
red = redis.Redis(host='192.168.1.11', port=6397, password='', decode_responses=True)
print(red.ping())  # 测试是否连接上

# 通过连接池获取redis对象连接服务器
poll = redis.ConnectionPool(host='192.168.1.11', port=6397, password='', decode_responses=True)
red = redis.Redis(connection_pool=poll) 
```

#### 应用场景
* 页面点击数
  * 对一系列页面需要记录点击次数
  * 例如论坛每个帖子都有记录点击次数，而点击次数比回帖次数多得多，使用关系型数据库存储点击会存在大量行级锁征用
  * 使用redis的INCR命令，让redis服务器启动时，可以从关系数据库读入点击数的初始值

* 主从复用，实现读写分离
  * 利用发布/订阅机制，Master Slave的模式，从Slave向Master发起SYNC命令
  * 可以是1 Master 多 Slave，可以分层，Slave下可以再接Slave，可以扩展成树形结构