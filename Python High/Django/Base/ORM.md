### 查询
* 原生数据库操作：
  * 语法：Model.objects.raw(sql语句，拼接参数)
  * 返回值：RawQuerySet集合对象，只支持基础操作，比如循环

#### 技巧
1. 利用__str__美化shell中的打印信息 
在model中设置了__str__属性后，在python manage.py shell中查询并打印，得到的QuerySet就会以__str__中的设置来显示
```
class Book(models.Model):
    pass 
    
    def __str__(self):
        return "%s|%s|%S".format(self.id, self.title, self.author)

form .models import Book
books = Book.objects.all()
# <QuerySet [<Book: 1|aaa|张三|>], [<Book: 2|bbb李四|>],...>
```

2. 利用.query打印django查询的对应的sql语句
```
books = Book.objects.all()
print(books.query)
```

3.F对象对某个表符合条件的数据进行更新
```
例1：跟新Book实例中所有零售价，涨10元
Book.objects.all().update(market_price=F('market_price')+10)
等价于sql语句：'UPDATE `bookstore_book` SET `market_price` = (`bookstore_book`, `market_price` + 10)'
等价于django ORM：
books = Book.objects.all()
for book in books:
    book.market_price=book.marget_price+10
    book.save()
# 应用：文章点赞。假设有个明星发了个微博，粉丝会在同一时刻进行非常多的点赞
def add_like(request, topic_id):
  # 取出文章
  topic = Topic.objects.get(id=topic_id)\
  # 高并发（许多人同时操作一行数据）时，这样写错误
  # 相当于：update topic set like =  1 where id = xxx
  topic.like = topic.like + 1
  topic.save()
  # 正确写法：使用F对象
  # 这样写相当于sql语句：update topic set like = like + 1 where id = xxx
  # 能够利用Mysql的Innodb数据库的行锁，使一行数据同一时刻只能被一个用户修改，防止出现脏读
  topic.like = F("like") + 1
  topic.save()

例2：对数据库中两个字段的值进行比较，列出哪些书的零售价高于定价
from django.db.models import F
from bookstore.models import Book
books = Book.objects.filter(market_price__gt=F('price'))
# 相当于：SELECT * FROM `bookstore_book` WHERE `bookstore_book`.`market_price` > (`bookstore_book`.`price`)
for book in books:
    print(book.title, '定价：', book.price, '现价'， book.market_price)
  
```

4. Q对象。解决复杂的逻辑或|、逻辑非等操作
运算符：&与操作、|或操作、~非操作、&~与非（条件1成立且条件2不成立）
```
# 查找类型不是机械且价格低于50的书
Book.objects.filter(Q(market_price__lt=50)&~Q(type='机械'))
```