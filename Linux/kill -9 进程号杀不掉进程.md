#### 第一种方法
lsof -i:端口号 得到进程号
kill -9 进程号

#### 第二种方法
可以查看该进程的父进程
cat /proc/8888/status   //8888为不可kill掉进程号
找到PPid父进程号，然后依次kill父子进程

#### 第三种方法
kill -9 $(lsof -i:5000|awk '{if(NR==2)print $2}')

#### 第四种方法
参考：https://cloud.tencent.com/developer/article/1493641
查看进程树: pstree -ap|grep gunicorn  
销毁除主进程外的其他进程: kill -HUP 主进程号 
kill主进程]q:kill -9 主进程号
