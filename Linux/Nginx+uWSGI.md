#### 概念
* 证书
  * .crt文件：是证书文件，crt是pem文件的扩展名（有时候没有crt只有pem的，所以不要惊讶）
  * .key文件：证书的私钥文件（申请证书时如果没有选择自动创建CSR，则没有该文件）
  * .pem扩展名的证书文件采用Base64-encoded的PEM格式文本文件，可根据需要修改扩展名
* 代理模式
  * 反向代理
    * 我们的角色是局域网web服务
    * 我们对外提供服务，属于服务提供者
  * 正向代理
    * 网速慢/翻墙访问外网。通过给浏览器配置一个网速快的、可以翻墙的代理ip及端口号来解决
    * 首先请求代理服务器，然后代理服务器帮我们去快速访问国外的网站，对于这种代理方式，我们就称之为正向代理  
    * 正向代理的本质是我们作为被代理者去请求外部的资源，如果以生产者、消费者模式来区分，我们属于消费者

#### 参考资料
* Nginx服务器安装部署详细步骤：https://blog.csdn.net/threelifeadv/article/details/105802346
* Nginx+uWSGI+Django部署web服务器
https://blog.csdn.net/u012145252/article/details/82147440
* Django+uwsgi+nginx微信小程序环境搭建
https://www.imooc.com/article/42569
* Django项目如何获得SSL证书与配置HTTPS
https://www.jb51.net/article/211236.htm
* uWSGI+django+nginx的工作原理流程与部署历程
https://blog.csdn.net/c465869935/article/details/53242126
* 将Python-Django项目部署到阿里云服务器踩的坑（服务器、域名、项目配置）
https://blog.csdn.net/brytlevson/article/details/111319622

##Nginx
#### 一、功能
* 作为用户访问网站的入口，监听阿里云/腾讯云等域名管理模块发送过来的网站访问请求。Nginx的反向代理能防止服务端暴露ip和端口，解决常见的跨域问题。
* 前后端分离项目中，将前端打包项目放在nginx配置文件(nginx.conf)指向的文件路径或默认路径(/var/www/html)中，用户即可通过代理路径或本机ip+文件夹名称直接访问前端静态资源。

#### 二、安装
##### 安装 Nginx 前 必须安装 PCRE：https://www.jianshu.com/p/14c81fbcb401
##### ubuntu安装nginx（适用需要https）
* 进入/usr/local (一般都会安装在该路径下，放其他路径也可)
* 输入获取安装包命令 sudo wget http://nginx.org/download/nginx-1.14.2.tar.gz  (需要其他版本可以自行修改nginx版本)
* 解压获取的安装包  sudo tar -zxvf nginx-1.14.2.tar.gz
* 进入解压得到的文件夹  cd nginx-1.14.2
* 配置 ssl 模块  sudo ./configure --prefix=/usr/local/nginx --with-http_ssl_module 
（通过sudo apt-get install nginx安装的nginx可能会没有configure这个文件，导致Nginx若缺少SSL模块无法安装补充模块）
* 使用 make 命令编译  sudo make
* 如果编译出现  **./configure: error: the HTTP rewrite module requires the PCRE library.**错误，说明缺少pcre-devel，需要其他依赖库:
  * 安装PCRE:  sudo apt-get install libpcre3 libpcre3-dev  
  * 安装zlib:  sudo apt-get install libpcre3 libpcre3-dev  
  * 安装openssl  sudo apt-get install openssl libssl-dev 
* 离开nginx-1.14.2到上一级，ls如果没有看见nginx文件夹，进入nginx-1.14.2运行sudo make install,若看见/usr/local/nginx被创建，说明Nginx安装成功。
* 进入nginx。注意：该目录一开始只有conf、html、sbin等四个文件，需要在sbin中运行nginx才会创建其它文件.
* 启动Nginx。进入/usr/local/nginx/sbin，该目录下只有一个nginx文件
          运行:  sudo ./nginx 即可启动
          重启:  sudo ./nginx -s reload
          停止:  ps -ef|grep nginx
                 sudo kill 端口号 

##### 另一种安装方法(不推荐，仅记录，不适用需要https的情况)
* 参考网址
https://www.cnblogs.com/zhaoyingjie/p/6840616.html
* 安装
sudo apt-get install nginx
这种方法安装的Nginx的配置文件nginx.conf一般在/etc文件夹下
默认配置指向的html在/var/www/html下，如果直接把前端打包文件放在该文件夹下可以直接用ip/前端文件夹名称访问前端
个人习惯将nginx自己配置的前端放在/usr/share/nginx/html下，但其实前端存放路径可以随意，只要在nginx配置文件中设置即可。


##### 验证安装是否成功
(1)全局方法
启动:
* **cd /usr/local/nginx/sbin**
里面有一个名叫nginx的文件
运行: sudo ./nginx 
**注意： nginx启动后默认占用80端口**
* /etc/init.d/nginx start或  service nginx start

关闭:
/etc/init.d/nginx stop 或 service nginx stop
重启:
/etc/init.d/nginx restart  或  service nginx restart
查看运行状态:
ps -ef|grep nginx
![](https://img2023.cnblogs.com/blog/2346193/202301/2346193-20230130114050882-73355926.png)
service nginx status
![](https://img2023.cnblogs.com/blog/2346193/202301/2346193-20230130114111823-241303237.png)
在Nginx服务启动的状态下，重新加载nginx.conf这个配置文件:
service nginx reload 

#### 卸载
* 卸载nginx（按顺序运行，当配置nginx出错不知道如何变回初始状态时建议直接卸载）:
参考网址: https://www.jianshu.com/p/439cd2a7c84e
sudo apt-get remove nginx nginx-common # 卸载删除除了配置文件以外的所有文件。
sudo apt-get purge nginx nginx-common # 卸载所有，包括删除配置文件。
sudo apt-get autoremove # 在上面命令结束后执行，主要是卸载删除Nginx的不再被使用的依赖包。
sudo apt-get remove nginx-full nginx-common #卸载删除两个主要的包。
* 其他
  * linux彻底删除nginx
  https://www.jianshu.com/p/439cd2a7c84e
