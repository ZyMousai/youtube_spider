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

        # 每次运行的唯一标识
        self.uuid_str = str(uuid.uuid1())

        # todo 总共需要多少条数据，测试为20
        self.__need_data_num = 20

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
    def __down(body, num):
        for x in range(num):
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

            if con_num >= self.__need_data_num:
                break
            else:
                self.__down(body, 20)

    def __do_one(self):
        # 1.需求一
        print('=========开始处理需求一')
        contents_els = self.driver.find_elements_by_xpath(
            "//ytd-video-renderer//div[@id='dismissible']/div/div[@id='channel-info']/ytd-channel-name")[
                       :self.__need_data_num]
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
                # 处理第二步需要用到得数据
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
        # 拼接csv名字
        csv_name = now_day + "&" + self.keyword + "&" + 'one' + '&' + self.uuid_str + ".csv"
        # 拼接csv路径
        csv_path = f"./result/{csv_name}"
        df1.to_csv(csv_path, encoding='utf_8_sig')
        print(f'=========需求一完成，已写入文件，|文件名{csv_name}|')

        self.driver.close()
        self.driver.quit()

    def do_two(self):
        """
        处理需求二
        :return:
        """
        print('=========开始处理需求二')
        # todo 模拟数据, 正式运营处理的是self.duplication_list，而不是wait_info
        # wait_info = [
        #     {
        #         'author': 'NairoMK',
        #         'author_link': 'https://www.youtube.com/channel/UCTSCjjnCuAPHcfQWNNvULTw',
        #         'keyword': 'light',
        #         'auth_tag': 0
        #     }
        # ]

        # todo 正式运行使用这个
        wait_info = self.duplication_list

        # 2.需求二
        self.__create_opt()

        now_day = datetime.datetime.now().strftime("%Y-%m-%d")
        df2 = pd.DataFrame(columns=("抓取日期", "关键词", "作者名称", "认证状态", "粉丝数量", "作者频道链接",
                                    "2个月内视频观看总数", "2个月内视频发布总数", "2个月内视频平均观看数",
                                    "说明", "商务咨询", "位置", "注册时间", "观看总数"))

        for index, info in enumerate(wait_info):
            print(f'=========需求二：开始处理第{index + 1}条数据')
            # 打开链接
            driver = self.__create_driver()
            driver.get(info['author_link'])
            # 判断视频日期
            body = driver.find_element_by_tag_name('body')
            # 点击切换到视频标签
            driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div').click()
            time.sleep(5)

            while True:
                date_els = driver.find_elements_by_xpath("//*[@id='metadata-line']/span[2]")
                date_text_list = [date_el.text for date_el in date_els]
                if '2个月前' or '1年前' or '2年前' or '3个月前' or '4个月前' or '5个月前' or '6个月前' or '7个月前' \
                        or '8个月前' or '9个月前' or '10个月前' or '11个月前' in date_text_list:
                    break
                else:
                    self.__down(body, 5)

            time.sleep(5)
            # 获取两个月内得视频个数
            videos_el_list = []
            videos_els = driver.find_elements_by_xpath('//ytd-grid-video-renderer')
            for videos_el in videos_els:
                videos_date = videos_el.find_element_by_xpath(".//*[@id='metadata-line']/span[2]").text
                if '年' in videos_date:
                    break
                elif '月' in videos_date:
                    if '1个月前' == videos_date:
                        videos_el_list.append(videos_el)
                elif '小时' in videos_date or '天' in videos_date or '周' in videos_date:
                    videos_el_list.append(videos_el)
                else:
                    pass

            total_play_nums = 0
            # 获取两个月内视频播放总数
            for v_el in videos_el_list:
                play_nums = v_el.find_element_by_xpath(".//*[@id='metadata-line']/span[1]").text
                if '万' in play_nums:
                    curr_play_nums = float(play_nums.split('万')[0]) * 10000
                    total_play_nums += curr_play_nums
                else:
                    total_play_nums += float(play_nums.split('次')[0])

            # 两个月内平均观看数量
            mid_play_nums = total_play_nums / 2
            # 粉丝数量
            fans_num = driver.find_element_by_xpath('//*[@id="subscriber-count"]').text

            # 切换到简介
            driver.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[6]/div').click()
            time.sleep(3)
            # 说明
            description = driver.find_element_by_xpath('//*[@id="description"]').text
            # 位置
            address_els = driver.find_elements_by_xpath(
                '//*[@id="details-container"]/table/tbody/tr[2]/td[2]/yt-formatted-string')
            if address_els:
                address = address_els[0].text
            else:
                address = None
            # 注册时间
            si_date = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[2]/span[1]').text
            # 观看总数
            all_total_play_nums = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]').text
            # todo 商务咨询，需要过谷歌验证码
            b_aff = None

            """
                    df2 = pd.DataFrame(columns=("抓取日期", "关键词", "作者名称", "认证状态", "粉丝数量", "作者频道链接",
                                    "2个月内视频观看总数", "2个月内视频发布总数", "2个月内视频平均观看数",
                                    "说明", "商务咨询", "位置", "注册时间", "观看总数"))
            """
            # 完善df2
            df2.loc[index] = [now_day, self.keyword, info['author'], info['auth_tag'], fans_num, info['author_link'],
                              total_play_nums, len(videos_el_list), mid_play_nums, description, b_aff, address, si_date,
                              all_total_play_nums]
            print(f'=========需求二，第{index + 1}条数据处理完毕')

            driver.close()
            driver.quit()

            time.sleep(random.randint(2, 4))
        # 2.1需求二写入
        # 拼接csv名字
        csv_name = now_day + "&" + self.keyword + "&" + 'two' + '&' + self.uuid_str + ".csv"
        # 拼接csv路径
        csv_path = f"./result/{csv_name}"
        df2.to_csv(csv_path, encoding='utf_8_sig')
        print(f'=========需求一完成，已写入文件，|文件名{csv_name}|')

    def run(self):
        self.__open_browser_one()
        # 处理需求一
        self.__do_one()
        # 处理需求二
        self.do_two()

# ax = YSpider('light')
# ax.do_two()
