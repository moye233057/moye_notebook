#### 安装: 
* https://docs.docker.com/

#### 命令
* 查看已经连接的服务端口（ESTABLISHED）
netstat -a
* 查看所有的服务端口（LISTEN，ESTABLISHED）
netstat -ap
* 查看指定端口，可以结合grep命令：
netstat -ap | grep 8080
* 也可以使用lsof命令：
lsof -i:8888
* 查看docker状态
sudo docker -v
sudo systemctl status docker
* 启动docker
sudo systemctl start docker
* 停止docker服务
sudo systemctl stop docker.socket
sudo systemctl stop docker
* 查看正在运行的docker
docker ps
* 停止正在运行的docker
docker kill (CONTAINER ID)
* 查看所有docker容器
docker ps -a
* 删除docker容器
docker rm (CONTAINER ID)

#### 技巧
* 在已发布的docker容器中修改其代码
https://blog.csdn.net/figosoar/article/details/111603539

#### 报错：
* Error response from daemon: conflict: unable to delete (cannot be forced)
https://blog.csdn.net/lctlinger/article/details/112764705