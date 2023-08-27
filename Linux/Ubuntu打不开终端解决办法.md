#### 一、按Ctrl+Alt+F1进入命令行模式，输入用户名或者密码登录
（注意：向日葵可能打不开，要到主机上操作）
#### 二、在终端输入： gnome-terminal
* 会遇到两种情况：
  * 第一种： ImportError: cannot import name 库名
    参考：https://blog.csdn.net/xuanlang39/article/details/105157332  里的步骤操作
  * 第二种： Failed to connect to Mir:Failed to connect to server socket
    参考：https://blog.csdn.net/qq_18649781/article/details/91492969
    1. 命令行输入： export DISPLAY=:0 
    2. sudo vim /etc/sudoers
    3. 在所有Defaults最新新增一行：Defaults env_keep+="DISPLAY"
    4. 执行完1或3之后，还可能会出现新的错误:
      Error constructing proxy for :1.69:/org/gnome/Terminal/Factory0
    5. 错误参考：https://blog.csdn.net/tianzhilan4444/article/details/118638928
      sudo apt-get install terminator
      dbus-launch gnome-terminal
#### 三、Ctrl+Alt+F7返回图形界面，看终端是否能打开
#### 四、第二步的第二种方法操作后，仍然无法在图形界面打开终端
1. Ctrl+Alt+F1进入命令行模式
2. 输入export NO_AT_BRIDGE=1
3. 输入export DISPLAY=:0
  * 注意：2和3步骤可以简化：
    * sudo vim /etc/environment/
    * 填入：
      NO_AT_BRIDGE=1
      DISPLAY=:0
    * 这样开机重启的时候会自动加上这两个环境变量
  * 参考： https://unix.stackexchange.com/questions/532585/getting-dbind-warnings-about-registering-with-the-accessibility-bus
4. 输入dbus-launch gnome-terminal
5. Ctrl+Alt+F7返回图形界面会发现已经打开了一个终端，仍旧无法在侧边栏新建终端或锁定到任务栏
6. 但是我们可以在这个终端输入gnome-terminal来新建终端

五、ubuntu切换不同用户的图形界面黑屏的问题
* 参考：https://blog.csdn.net/appleyuchi/article/details/115166066
* 用第四步的方法调出终端
* 以某个服务器为例：
  * 切换到root用户: su root
  * 修改文件：sudo vim /etc/default/grub
  * 修改配置：将GRUB_CMDLINE_LINUX_DEFAULT="quiet splash" 修改为GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"
  * 重启系统：sudo reboot
  * 用不能切换的用户登录