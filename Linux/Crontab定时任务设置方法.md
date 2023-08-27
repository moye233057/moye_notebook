#### 一、命令
crontab -l 表示列出所有的定时任务
crontab -r 表示删除用户的定时任务，当执行此命令后，所有用户下面的定时任务会被删除，执行crontab -l后会提示用户： no crontab for admin
crontab -e 设置定时任务
参考：https://blog.csdn.net/woshiyangyunlong/article/details/99944576

#### 二、操作步骤
* crontab -e 进入定时任务编辑状态
* 在最下方添加一行定时任务，例如: 0 10 * * * sh /home/root/copyfile.sh > /home/root/copyfile.log
* ctrl+x 退出编辑状态，此时会出现提示: Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES)？YES  NO
* 按Y键同意修改，会出现提示：File Name to Write: /tmp/crontab...
* 按enter键同意本次修改写入本地文件
  * 如果你的修改有误，例如小时设置了24，超过范围，会报错:errors in crontab file, can't install
  * 如果修改无误，会提示：crontab：installing new crontab


#### 三、实例
```
# 例1：
# 每天十点运行/home/root/下的copyfile.sh脚本，并把结果记录在/home/root/下的copyfile.log文件中
0 10 * * * sh /home/root/copyfile.sh > /home/root/copyfile.log
# crontab文件中的行由6个字段组成，不同字段间用空格或者tab键分割。前5个字段指定命令要运行的时间
分钟（0-59）
小时（0-28）
日期（1-31）
月份（1-12）
星期几（0-6，其中0代表星期日）
第六个字段是一个要在适当时间执行的字符串

# copyfile.bash内容
#!/bin/bash

#设置环境变量
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin

#复制项目
sudo cp -r /home/trizhi2/project /home/beifen

#判断是否备份成功        
if [ $? -ne 0 ];then
    echo “备份失败”
else
    echo "备份成功"
fi


# 例2：
# settings.py中利用django-crontab设置定时任务
INSTALLED_APPS = [
  ...
  django_crontab
  ...
]

# 定时任务
'''
*    *    *    *    * ：分别表示 分(0-59)、时(0-23)、天(1 - 31)、月(1 - 12) 、周(星期中星期几 (0 - 7) (0 7 均为周天))
crontab范例：
每五分钟执行    */5 * * * *
每小时执行     0 * * * *
每天执行       0 0 * * *
每周一执行       0 0 * * 1
每月执行       0 0 1 * *
每天23点执行   0 23 * * *
'''
CRONJOBS = [
    ('0 12 * * *', 'xxx.method', ' >> /tmp/logs/confdict_handle.log'), 
]
# xxx.method对应方法在项目中的路径，从根目录的下一级开始
# 设置并运行项目后，会在Linux的crontab中出现对应的定时任务，例如：
# 0 12 * * * /usr/bin/python3 /home/root/project/manage.py crontab run 49a013ee87bc14105bdb8b0393313302  >> /tmp/logs/confdict_handle.log # django-cronjobs for expatents
```