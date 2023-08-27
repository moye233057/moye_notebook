### 一、概念
* **内网:** 局域网，同一局域网的内网ip不相同
* **外网:** 互联网，局域网通过一台服务器或是一个路由器对外连接的网络，这个IP地址是唯一的。也就是说内网里所有的计算机都是连接到这一个外网IP上，通过这一个外网IP对外进行交换数据的。也就是说，一个局域网里所有电脑的内网IP是互不相同的,但共用一个外网IP。（用ipconfig/all查到的IP是你本机的内网IP；在[http://www.ip138.com]()上看到的是你连接互联网所使用的IP，即外网）。
* **公有IP:** 能够直接访问互联网，公有IP资源有限，一般是一个或多个局域网共用一个公有IP上网
* **私有IP:** 不能够直接访问互联网
* **端口映射:** 是 NAT 的一种，它将外网主机的 IP 地址的一个端口映射到内网中一台机器，提供相应的服务。当用户访问该 IP 的这个端口时，服务器自动将请求映射到对应局域网内部的机器上。

### 二、原理
* 让在内网的节点主动访问一个拥有公网IP地址的服务器，并由中间服务器搭桥，打通经过该服务器从其他主机到NAT之后节点的隧道。
* 一般的内网穿透工具进行配置时，会先在要穿透访问的局域网机器中运行内网穿透软件，只需要配置该机器在局域网的ip和访问端口，以及公网映射的地址即可。之所以没有外网IP，个人理解是由于局域网的外网IP的唯一性，运行工具的时候就能够自动获取这个对外ip，无需用户填写。

### 三、部分软件使用
#### （1）ubuntu花生壳
花生壳在局域网机器下载向日葵盒子,记录安装产生的SN码和密码,安装完成后可以用phddns
查看扩展功能，phddns start（启动服务）
启动后还需要在浏览器输入地址进行登录：
https://console.hsk.oray.com/passport/login
开通内网穿透服务具体参考花生壳官网：
https://hsk.oray.com/
花生壳相当于以自己的服务器作为中介，会提供一个花生壳的公网地址，防止公网地址重复

#### （2）natapp
参考: https://blog.csdn.net/weixin_41979531/article/details/128259713

### 四、Python内网穿透代码
* Python的paramiko模块，能够远程连接到服务器，实现运行脚本文件及文件上传下载两个主要功能
* 在paramiko的exec_commend中，例如: python /home/xxx.py args[1] args[2] ...
  * python代表运行命令用到的环境，python是默认环境，也可以根据服务器本地的环境进行修改，例如/home/anaconda3/bin/python
  * xxx.py代表运行的脚本的绝对路径
  * args[1] args[2]... 代表传入的参数，注意空格分隔，不要带其他字符例如"-"，每一个args代表一个参数，在脚本中用sys.argv[n]来获取对应参数
* 实战案例
  * 案例1
  ```
  """
  有一个只在局域网运行的elasticsearch搜索引擎，需要用内网穿透获取数据
  具体思路是：通过paramiko.SSHClient()访问Linux服务器，利用exec_command运行：python 脚本文件路径 -参数 ，得到数据
  """
  # ssh代码
  import paramiko
  text = "阅读"
  # 创建SSH对象
  ssh = paramiko.SSHClient()
  # 允许连接不在know_hosts文件中的主机
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  # 连接服务器
  ssh.connect('映射的公网', username='ssh用户名', password='ssh密码', port=内网穿透端口, timeout=1500)
  # 执行命令
  stdin, stdout, stderr = ssh.exec_command("python /home/username/PythonFile.py -{}".format(text))
  # 返回的stdout对应脚本最后的print内容
  out = bytes.decode(stdout.read(), encoding="utf-8")
  print(out)

  # PythonFile.py脚本代码
  import sys
  from elasticsearch import Elasticsearch
  from elasticsearch_dsl import Search
  # sys.argv[1]代表命令行命令的第一个参数
  text = sys.argv[1]
  client = Elasticsearch("内网ip:内网端口")
  s = Search(client, index="index_name").query("match", title=text)
  response = s.execute()
  result = []
  for hit in response:
      result.append({
          "title": hit.title,
          "content": hit.content,
  })
  print(result)
  ```

  * 案例2
  ```
  # 输入是文章撰写系统的每一段的基础信息，包括段落id、标题、正文、举例，处理是用elasticsearch根据每一段正文进行相似度比较，得到可能相似的文段及相似度，最后以输入的段落顺    
  序输出相似度分析结果
  # 思路：先用SFTP在内网服务器创建空白文件，再将每一段的基本信息以分隔符分隔放在一行，逐行存入内网文件中；然后用exec_command运行本地脚本，本地读取文件获得数据，多线程在elasticsearch中获取相似段落及相似度
  
  # 内网创建空白文件，逐行写入数据
  ids = [] # 每一段的id
  tits = [] # 每一段的标题
  cons = [] # 每一段的正文
  exas = [] # 每一段的例子
  title = "filename"  # 标题(文件名)
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect('xxx', port=8888, username='xxx', password='xxx')
  sftp = ssh.open_sftp()
  remote_file_path = '/home/truebash/data/{}.txt'.format(title)
  with sftp.open(remote_file_path, 'wb') as remote_f:
      for i, id in enumerate(ids):
          content = id + '  ' + tits[i].strip('\n') + '  ' + cons[i].strip('\n') + '  ' + exas[i].strip('\n') + '\n'
          file_stream = io.BytesIO(content.encode())
          remote_f.write(file_stream.read())

  sftp.close()
  ssh.close()


  # 执行命令，本地读取文件
  ssh = paramiko.SSHClient()
  # 允许连接不在know_hosts文件中的主机
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  # 连接服务器
  ssh.connect('xxx', username='xxx', password='xxx', port=8888, timeout=60,
              allow_agent=False, look_for_keys=False)
  stdin, stdout, stderr = ssh.exec_command(r"python /home/truebash/assess_report.py {}".format(title))
  # 使用SSHClient对象的settimeout()方法来设置exec_command()命令的超时时间
  stdout.channel.settimeout(30)
  print("stderr:", stderr.read())
  # print("stdout:", stdout.read())
  count = 0
  out = ''
  while not stdout.channel.exit_status_ready():
      time.sleep(1)
      if stdout.channel.exit_status_ready():
          out = stdout.read()
          # 将ssh返回的字节转换为字符串
          out = bytes.decode(out, encoding="utf-8")
          break
      count += 1
      if count == 15:
          break

  # 内网服务器对应的脚本assess_report.py
  # coding: utf-8
  import codecs
  import sys
  from elasticsearch import Elasticsearch
  from elasticsearch_dsl import Search
  from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED

  def contentforsimilar(line):
      line = list(filter(None, line))
      """检索es查找文本对应的es相似文本"""
      try:
          cid = line[0]
          title = line[1]
          content = line[2]
      except:
          # print(line)
          return
      s = Search(using=client, index="pat_all").query("match", summary=content)
      s = s[:10]
      res = s.execute()
      sims = []
      for hit in res:
          score = hit.meta.score
          if score > 5:
              # print(hit.meta.score)
              summary = hit.summary
              # print(hit.summary)
              # print("-"*10)
              sims.append({
                  "score": score,
                  "summary": summary,
              })
              if len(sims) == 3:
                  break
      res = {
          "cid": cid,
          "title": title,
          "sims": sims
      }
      return res


  try:
      title = sys.argv[1]
  except:
      title = "优惠券效验"

  client = Elasticsearch("192.168.1.12:9203", timeout=60)

  file_path = r"/home/truebash/data/{}.txt".format(title)
  with codecs.open(file_path, 'r', 'utf_8_sig') as f:
      executor = ThreadPoolExecutor(max_workers=15)
      lines = f.readlines()
      lines = [line.split(' ') for line in lines]
      # 获取id列表，因为id有1-1的形式，取第一个字符校验是不是正确的序号，如果不是说明这一行的格式出错，不进行分析
      ids = []
      for line in lines:
          try:
              cid = line[0]
              int(cid[0])
              ids.append(cid)
          except:
              continue
      # print(ids)
      returndata = []
      # 线程池，多线程进行es相似度匹配
      with executor as pool:
          tasks = []
          for line in lines:
              tasks.append(pool.submit(contentforsimilar, line))
          # 等待到第一个线程任务执行完毕
          wait(tasks, return_when=FIRST_COMPLETED)
          for futrue in as_completed(tasks):
              data = futrue.result()
              returndata.append(data)
      returndata = sorted(returndata, key=lambda x: ids.index(x['cid']))
  print(returndata)

  # 案例3：针对案例2进行改进
  # 不再将相似度的json结果直接返回，而是在内外服务器本地生成文档，然后外网服务器用sftp.get(remote_path, local_path)将文件下载下来，最后把外网服务器存储文件的地址返回给前端
  ```

### 五、遇到的错误。
(1)Error reading SSH protocol banner
(2)paramiko.ssh_exception.NoValidConnectionsError: [Errno None] Unable to connect to port xxx on 0.0.0.0
尝试解决问题：
* 先查看运行脚本命令的返回结果：
```
stdin, stdout, stderr = ssh.exec_command("python /home/username/PythonFile.py -{}".format(text))
stdout能接收脚本打印出来的信息
stderr能接收脚本出现的错误信息，优先查看这个错误信息判断问题所在
```
* 由于是用ssh链接ubuntu系统，怀疑是短时间ssh请求过多，当时timeout设置为1500,可能达到上限
在ubuntu系统中，命令行输入:ps -ef|grep ssh
kill掉无用的ssh连接端口
* 以后端接口作为跳板请求了脚本文件，怀疑可能是后端建立太多ssh连接没有及时关闭。
将ssh的过期时间timeout设置小点，并且在接口最后加上ssh.close()及时关闭当前连接，最后重启后端项目
(3)exec_command运行脚本时，出现no module name six
* 首先要检测环境是否有对应的包
  ```
  # 查看当前环境的python路径
  which python
  # 查看所有的python环境
  whereis python
  # 或者去系统默认python环境中找
  cd /usr/local/lib
  ls
  cd python2.7/site-packages/
  ls
  ```
* 尝试指定脚本的运行环境
  ```
  方式一：
  # python默认环境，/home/anaconda3/bin/python指定anaconda3的base环境
  exec_commend('指定的python环境 脚本路径 参数')
  方式二：
  在.py脚本文件的顶部加入一行指定运行环境
  #！/home/anaconda3/bin/python
  ```
* 以上两个都不行，下面是个人原因造成的错误
  * 原因：ssh连接用的用户名与脚本存放的用户目录不一致
  * 关键代码： 
  ```
  ssh.connect('xxx', username='user1_name', password='user1_pass', port=8888, timeout=60,
              allow_agent=False, look_for_keys=False)
  stdin, stdout, stderr = ssh.exec_command(r"python /home/user2/truebash/assess_report.py {}".format(title))
  ```
  * 可以看到，用connect连接时我用的是user1的账户，那么他对应的用户目录应该为user1,但是我的脚本文件放在了user2中，这样就会出现user1没有权限访问user2文件的情况，导致命令运行失败，出现上面的错误
  * 解决办法：connect用的用户和脚本文件存放用户目录进行统一，user1连接，脚本就放user1的用户目录 