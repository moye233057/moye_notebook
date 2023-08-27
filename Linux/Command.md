#### 一、系统信息
```
# 查看Linux系统位数
getconf LONG_BIT
## linux服务器出现大量连接：sshd: root@notty
# 查看ssh链接的信息
netstat -antup | grep ssh
# 查看内核版本与发行版本
https://www.cnblogs.com/suyuan1573/p/6185302.html
# 查看系统进程上限
ulimit -u
# 查看大小（stack size (kbytes,-s)表示线程堆栈大小，一般常见的有10M或者是8M
ulimit -s

# 查看pip镜像源
pip config list

# 关闭当前用户的ssh链接
ps auxf | grep notty | awk '{print $2}' |xargs kill -9
```

#### 二、进程
```
# 参考：https://cloud.tencent.com/developer/article/1711858
# ps命令用于报告当前系统的进程状态。可以搭配kill指令随时中断、删除不必要的程序。
# ps命令是最基本同时也是非常强大的进程查看命令，使用该命令可以确定有哪些进程正在运行和运行的状态、进程是否结束、进程有没有僵死、哪些进程占用了过多的资源等等
# 查看所有进程四种方法
* ps aux
  * a：显示当前终端下的所有进程信息，包括其他用户的进程
  * u：使用以用户为主的格式输出进程信息
  * x：显示当前用户在所有终端下的进程
* ps -elf
  * -e：显示系统内的所有进程信息
  * -l：使用长（long）格式显示进程信息
  * -f：使用完整的（full）格式显示进程信息。
* top
* pstree -aup  # 以树状图的方式展现进程之间的派生关系，显示效果比较直观
# 查看指定端口号进程情况
netstat -tunpl | grep 3306
# 查看某一进程占用端口，例如python
ps -ef |grep python
# 杀死某一个端口号的进程，-s代表强制杀死
kill [-s] 3306
# 查看进程的工作路径
* 找到目标进程的pid
  * ps -ef|grep 进程名
* 方法一
  * pwdx pid
* 方法二
  * ll /proc/pid/cwd
```

三、端口
```
# 查看800端口的占用情况
lsof -i:8000
# 关闭对应的端口的程序
sudo kill -9 PID
```

用户信息
```
列出详细用户信息
cat /etc/passwd
仅保留简单用户注册信息：
cat /etc/passwd |cut -f 1 -d:
```

文件查找
* 参考：https://blog.csdn.net/xxmonstor/article/details/80507769
* 查找的命令主要有find和grep
* 区别：
  * find命令是根据文件的属性进行查找，如文件名，文件大小，所有者，所属组，是否为空，访问时间，修改时间等。
    * 格式： find path 属性 内容
    * 例如： find / --name redis 在根目录下查找redis路径
  * grep是根据文件的内容进行查找，会对文件的每一行按照给定的模式(patter)进行匹配查找。
  * which       查看可执行文件的位置 ，只有设置了环境变量的程序才可以用
  * whereis    寻找特定文件，只能用于查找二进制文件、源代码文件和man手册页
  * locate       配合数据库查看文件位置 ,详情：locate -h查看帮助信息

文件信息
```
# 查看系统总大小
df
# 查看当前文件目录文件夹大小
du -h --max-depth=1
# 查看运行中的服务的安装目录
  # 查看进程号
  ps -ef|grep redis
  # 依据进程号查看安装路径
  ls -l /proc/进程号/cwd
``