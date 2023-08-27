#### 什么是单元测试
* 针对程序模块进行正确性检验
* 一个函数，一个类进行验证
* 自底向上保证程序正确性

#### 为什么要写单元测试
三无代码不可取（无文档、无注释、无单测）
* 保证代码逻辑的正确性
* 单测影响设计，易测的代码往往是高内聚低耦合的
* 回归测试，防止改一处整个服务器不可用

#### 单元测试相关库
* nose/pytest较为常用
* mock模块用来模拟替换网络请求
* coverage统计测试覆盖率

#### 单元测试例子
```
def test():
  """
  如何设计测试用例：（等价类划分）
  - 正常值功能测试
  - 边界值（比如最大最小，最左最右值）
  - 异常值（比如None， 空值， 非法值）
  """
  # 正常值
  assert b_search([1, 2, 3], 1) == 1
  assert b_search([1, 2, 3], 6) == -1
  # 边界值
  assert b_search([1, 2, 3], 0) == 0
  # 异常值
  assert b_search([], 1) == -1
```