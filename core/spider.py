"""
处理需求一及整体流程
"""
import random
import time
import uuid

import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class YSpider(object):
    """youtube spider"""
    UA_LIST = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3975.2 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4183.102 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
    ]

    def __init__(self, keyword):
        self.keyword = keyword

        self.__base_url = 'https://www.youtube.com/'

        self.__url = f'{self.__base_url}results?search_query={keyword}'

        self.__headers = {
            'user-agent': random.choice(self.UA_LIST)
        }

        self.__chrome_path = './tools/Chrome/chrome.exe'

        self.__chrome_driver_path = './tools/Chrome/chromedriver.exe'

        self.__js_path = './tools/Chrome/stealth.min.js'

        self.__webrtc_path = './tools/Chrome/webrtc.crx'

        self.__opt = None

        self.__driver = None

    def __create_opt(self):
        self.__opt = webdriver.ChromeOptions()

        # https忽略证书错误
        self.__opt.add_argument('--ignore-certificate-errors')
        # 指定ua
        self.__opt.add_argument('--user-agent=%s' % random.choice(self.UA_LIST))
        # 添加webrtc
        self.__opt.add_extension(self.__webrtc_path)
        # 不显示测试软件正在控制的消息
        self.__opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.__opt.add_experimental_option("detach", True)
        # 二进制方式指定浏览器路径
        self.__opt.binary_location = self.__chrome_path

    def __create_driver(self):
        driver = webdriver.Chrome(executable_path=self.__chrome_driver_path, options=self.__opt)

        with open(self.__js_path) as f:
            js = f.read()
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": js
        })

        return driver

    @staticmethod
    def __down(body):
        for x in range(20):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.uniform(0.3, 0.5))

    def __open_browser_one(self):
        self.__create_opt()
        self.driver = self.__create_driver()
        self.driver.get(self.__url)

        body = self.driver.find_element_by_tag_name('body')

        time.sleep(5)
        while True:
            con_num = len(self.driver.find_elements_by_xpath("//ytd-video-renderer"))

            if con_num >= 20:
                break
            else:
                self.__down(body)

    def __do_one(self):
        # 1.需求一
        print('=========开始处理需求一')
        contents_els = self.driver.find_elements_by_xpath(
            "//ytd-video-renderer//div[@id='dismissible']/div/div[@id='channel-info']/ytd-channel-name")[:1000]
        # 建立处理csv所需数据
        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        df1 = pd.DataFrame(columns=("抓取日期", "关键词", "作者名称", "认证状态", "作者频道链接"))

        # 去重用list
        de_duplication_list = []
        # 去重后得list
        self.duplication_list = []
        print(f'=========成功拿到{len(contents_els)}条数据')
        print('=========开始处理数据')
        # 处理拿到得数据
        for index, con_els in enumerate(contents_els):
            author_el = con_els.find_element_by_xpath(".//a")
            # 获取作者名称
            author = author_el.text
            # 获取作者频道链接
            author_link = author_el.get_attribute('href')
            # 获取作者认证状态
            auth_tag_el = con_els.find_elements_by_xpath("./ytd-badge-supported-renderer/div")
            author_tag = 1 if auth_tag_el else 0

            if author_link not in de_duplication_list:
                # 处理第二部需要用到得数据
                self.duplication_list.append({
                    "author": author,
                    "author_link": author_link,
                    "auth_tag": author_tag,
                    "keyword": self.keyword
                })

                # 完善df1
                df1.loc[index] = [now_day, self.keyword, author, author_tag, author_link]

                # 去重
                de_duplication_list.append(author_link)
        print(f'=========去重后数据还剩{len(de_duplication_list)}条数据')
        # 1.1 写入csv
        # 每次运行的唯一标识
        uuid_str = str(uuid.uuid1())
        # 拼接csv名字
        csv_name = now_day + "&" + self.keyword + "&" + 'one' + '&' + uuid_str + ".csv"
        # 拼接csv路径
        csv_path = f"./result/{csv_name}"
        df1.to_csv(csv_path, encoding='utf_8_sig')
        print(f'=========需求一完成，已写入文件，|文件名{csv_name}|')

        self.__close_driver()

    def do_two(self):
        """
        抓取日期 | 关键词 | 作者名称 | 认证状态 | 粉丝数量 | 作者频道链接 | 2个月内视频观看总数 | 2个月内视频发布总数 | 2个月内视频平均观看数 | 说明 | 商务咨询 | 位置 | 注册时间 | 观看总次数
        """
        wait_info = [
            {
                'author': 1,
                'author_link': 'https://www.youtube.com/channel/UCTSCjjnCuAPHcfQWNNvULTw',
                'keyword': 'light',
                'auth_tag': 0
            }
        ]
        self.__create_opt()
        for index, info in enumerate(wait_info):
            # 打开链接
            driver = self.__create_driver()
            driver.get(info['author_link'])

            # 判断视频日期
            body = self.driver.find_element_by_tag_name('body')

            # todo

            driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div').click()
            time.sleep(3)

    def __close_driver(self):
        self.driver.close()
        self.driver.quit()

    def run(self):
        self.__open_browser_one()
        # 处理需求一
        self.__do_one()
        # 处理需求二
        self.do_two()


ax = YSpider('123')
ax.do_two()
