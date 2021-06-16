"""
spider
"""
import random
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from csv_handle import CsvHandle


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
        driver = webdriver.Chrome(executable_path=self.__chrome_driver_path, chrome_options=self.__opt)

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

    def __open_browser(self):
        self.__create_opt()
        self.driver = self.__create_driver()
        self.driver.get(self.__url)

        body = self.driver.find_element_by_tag_name('body')

        time.sleep(5)
        while True:
            con_num = len(self.driver.find_elements_by_xpath("//ytd-video-renderer"))

            if con_num >= 20:
                print(con_num)
                break
            else:
                self.__down(body)
            print(con_num)

    def __do(self):
        # 1.需求一
        # 抓取日期 | 关键词 | 作者名称 | 认证状态 | 作者频道链接
        contents_els = self.driver.find_elements_by_xpath(
            "//ytd-video-renderer//div[@id='dismissible']/div/div[@id='channel-info']/ytd-channel-name")

        csv_info = []
        for con_els in contents_els:
            author_el = con_els.find_element_by_xpath(".//a")
            author = author_el.text
            author_link = author_el.get_attribute('href')

            auth_tag_el = con_els.find_elements_by_xpath("./ytd-badge-supported-renderer/div")
            csv_info.append({
                "author": author,
                "author_link": author_link,
                "auth_tag": auth_tag_el,
                "keyword": self.keyword
            })

        # 1.1 写入csv
        CsvHandle.tag = 1
        CsvHandle.create_csv(csv_info)
        # 2.需求二

    def run(self):
        self.__open_browser()
        self.__do()
