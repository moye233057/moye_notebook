#### 执行系统命令，并拿到命令的结果
```
# 能够执行，但是res返回的不是结果而是标志位，成功会返回0，
import os
res = os.system('ls /')
print('命令的结果：' res)
# 实际执行系统命令需要用subprocess
# subprocess能够调用程序（shell=True）解析命令
# stdout=subprocess.PIPE(管道)：将命令产生的结果丢到管道中，管道中的数据取走一次就没了，不能再取
import subprocess
obj = subprocess.Popen('ls /', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(obj)
print('stdout 1--->:', obj.stdout.read()) # read拿到的结果类型为bytes，正好是C/S间通信需要的格式
```