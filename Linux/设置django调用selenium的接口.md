#### 第一步：安装chrome
* wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
* sudo apt install ./google-chrome-stable_current_amd64.deb
* 查看版本号: google-chrome --version  # 112.0.5615.49 
* export DISPLAY=:0
* export PATH=$PATH:/opt/google/chrome/


#### 第二步：安装chromedriver
通过上面查到的版本号，替换路径中的“版本号”，下载合适的driver
wget http://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip
 
解压
unzip chromedriver_linux64.zip
 
移动到启动路径
mv chromedriver /usr/local/bin/
 
分配权限
chmod 777 /usr/local/bin/chromedriver
 
查看版本号
chromedriver --version


#### 第三步：下载selenium
pip install selenium

#### 第四步：编写接口函数：
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")  # 将浏览器静音

如果遇到
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally.
(unknown error: DevToolsActivePort file doesn't exist)，加上下面两行
chrome_options.add_argument('--no-sandbox')  # 沙盒模式运行
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

chrome_options.add_argument("--headless")  # 无界面模式
chrome_options.add_argument("--disable-gpu")  # 禁用gpu渲染
chrome_options.add_argument('--disable-dev-shm-usage') # 大量渲染时候写入/tmp而非/dev/shm
binary_location是安装的chrome的路径
/usr/local/bin/chromedriver是第二步driver的安装路径，可以用whereis chromedriver查看
chrome_options.binary_location = '/opt/google/chrome/chrome'
driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')  


#### 卸载
sudo apt purge google-chrome-stable
cd ~/.config
rm -rf google-chrome

sudo rm -f /usr/bin/chromedriver
