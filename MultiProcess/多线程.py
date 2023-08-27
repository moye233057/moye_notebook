import queue
import random
import threading
import time
import requests
from resources import urls
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
"""
可以用：time curl http://ip:port/xxx 来测试响应时间
"""



def craw(url):
    """根据传入的url发送请求，获取页面内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
    }
    r = requests.get(url, headers=headers)
    # print(url, len(r.text))
    return r.text


def parse(html):
    """解析内容"""
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="post-item-title")
    return [(link["href"], link.get_text()) for link in links]


class base_multi_thread:

    def multi_thread(self, num=-1):
        threads = []
        for url in self.urls[:num]:
            threads.append(
                threading.Thread(target=craw, args=(url,))
            )

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


class ProducerConsumer:
    def __init__(self, url_queue, html_queue):
        self.url_queue = url_queue
        self.html_queue = html_queue

    def do_craw(self):
        count = 0
        while True:
            url = self.url_queue.get()
            if not url and count < 3:
                count += 1
                continue
            if count >= 3:
                break
            html = craw(url)
            self.html_queue.put(html)
            time.sleep(random.randint(1, 2))

    def do_parse(self, fout):
        count = 0
        while True:
            html = self.html_queue.get()
            if not html and count < 3:
                count += 1
                continue
            if count >= 3:
                break
            results = parse(html)
            for result in results:
                fout.write(str(result) + "\n")
            time.sleep(random.randint(1, 2))

    def run(self):
        for url in urls:
            self.url_queue.put(url)
        print(self.url_queue.qsize())

        for idx in range(3):
            t = threading.Thread(target=self.do_craw, name=f"craw{idx}")
            t.start()

        fout = open("result.txt", "w")
        for idx in range(2):
            t = threading.Thread(target=self.do_parse, args=(fout,), name=f"parse{idx}")
            t.start()


class ThreadPoolObj:

    def __init__(self):
        pass

    def method1(self):
        """会按顺序打印结果"""
        with ThreadPoolExecutor() as pool:
            results = pool.map(craw, urls)
            for result in results:
                print(result)

    def method2(self):
        """哪个线程先结束就先打印哪个线程的结果"""
        with ThreadPoolExecutor() as pool:
            futures = [pool.submit(craw, url) for url in urls]
            for future in futures:
                print(future.result())
            for future in as_completed(futures):
                print(future.result())


if __name__ == '__main__':
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    PC = ProducerConsumer(url_queue, html_queue)
    PC.run()
