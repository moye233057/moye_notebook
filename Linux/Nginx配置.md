#### 参考资料
  * Nginx的配置详解：https://www.cnblogs.com/zengfp/p/9897026.html
  * Nginx的高级使用：https://zhuanlan.zhihu.com/p/406914439
  * Nginx应用：https://zhuanlan.zhihu.com/p/368785355
  * Nginx 配置 HTTPS 完整过程：https://blog.csdn.net/weixin_37264997/article/details/84525444/
  * Nginx配置SSL证书：https://www.cnblogs.com/zeussbook/p/11231820.html
  * Vue打包部署到Nginx时,css样式不生效的解决方式：https://www.jb51.net/article/192416.htm
  * Nginx出现500 Internal Server Error 错误的解决方案：	https://cloud.tencent.com/developer/article/1725936

#### 放最外层http{}的设置
```
#隐藏版本号
server_tokens on;
#优化服务器域名的散列表大小 
server_names_hash_bucket_size 64;
server_names_hash_max_size 2048;

#开启高效文件传输模式，同时将tcp_nopush_on和tcp_nodelay on两个指令为on，可防止网络及磁盘I/O阻塞，提升Nginx工作效率
sendfile on;
tcp_nopush on; 

keepalive_timeout  300;

# 502 bad gateway 错误解决配置 start
uwsgi_buffer_size 16k;
uwsgi_busy_buffers_size 24k;

proxy_buffer_size 64k;
proxy_buffers 32 32k;
proxy_busy_buffers_size 128k;
large_client_header_buffers 4 16k;
client_max_body_size 300m;
client_body_buffer_size 128k;
proxy_connect_timeout 600;
proxy_read_timeout 600;
proxy_send_timeout 600;
proxy_temp_file_write_size 64k;

fastcgi_connect_timeout 300;
fastcgi_send_timeout 300;
fastcgi_read_timeout 300;
# 502 bad gateway 错误解决配置 end
```

#### 放server{}里面的设置
```
## 通用配置
# 允许跨域请求的域名，*代表所有
add_header 'Access-Control-Allow-Origin' *;
# 允许带上cookie请求
add_header 'Access-Control-Allow-Credentials' 'true';
# 允许请求的方法，例如：GET、POST、PUT、DELETE等，*代表所有
add_header 'Access-Control-Allow-Methods' *;
# 允许请求的头信息，例如：DNT,X-Mx-ReqToken,Keep-Alive,User-Agent等，*代表所有
add_header 'Access-Control-Allow-Headers' *;

## listen 80配置;
# 不允许python和curl命令的请求
if ($http_user_agent ~* (Python|Curl)) {
    return 403;
}
# 重定向到443端口，https
rewrite ^/(.*)$ https://www.xxx.com:443/$1 permanent;

## listen 443配置
## pem和key是https需要的ca证书相关文件，需要申请和下载
ssl_certificate       /usr/local/nginx/xxx.pem;
ssl_certificate_key       /usr/local/nginx/xxx.key;


```

#### 放location xxx {}里面的设置
```
# 禁止sh和bash脚本
location ~ .*\.(sh|bash)?$
{
        return 403;
}
# 域名80端口默认返回html页面，根据/usr/share/nginx/html
location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
}
# 普通的反向代理
location /media {
    proxy_pass http://59.110.237.12:8002;
}
# 与uwgsi进行通信
uwsgi_connect_timeout      600;   # 指定连接到后端uWSGI的超时时间。
uwsgi_read_timeout         600;        # 指定接收uWSGI应答的超时时间，完成握手后接收uWSGI应答的超时时间。
include /home/xxx/uwsgi_params;
uwsgi_pass ip:port;
```