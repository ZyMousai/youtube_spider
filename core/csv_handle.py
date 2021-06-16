import pandas as pd
import datetime


class CsvHandle(object):
    tag = 1

    @classmethod
    def create_csv(cls, csv_info):
        # 抓取日期 | 关键词 | 作者名称 | 认证状态 | 作者频道链接
        now_day = datetime.datetime.now().strftime("")
        if cls.tag == 1:
            heard = ["抓取日期", "关键词", "作者名称", "认证状态", "作者频道链接"]
        else:
            pass
