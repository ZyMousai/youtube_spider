"""
spider
"""
import random

import requests


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
        # self.__url = f'https://www.youtube.com/results?search_query={keyword}'
        self.__url = 'https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'

        self.__headers = {
            'user-agent': random.choice(self.UA_LIST)
        }

        self.__proxies = {
            "http": "socks5://127.0.0.1:5000",
            "https": "socks5://127.0.0.1:5000"
        }

    def run(self):
        data = {"context": {
            "client": {"hl": "zh-CN", "gl": "US", "remoteHost": "223.16.18.167", "deviceMake": "", "deviceModel": "",
                       "visitorData": "CgtxSHdqdHBDd3N5RSixjKGGBg%3D%3D",
                       "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36,gzip(gfe)",
                       "clientName": "WEB", "clientVersion": "2.20210613.07.00", "osName": "Windows",
                       "osVersion": "10.0", "originalUrl": "https://www.youtube.com/results?search_query=light",
                       "platform": "DESKTOP", "clientFormFactor": "UNKNOWN_FORM_FACTOR", "timeZone": "America/New_York",
                       "browserName": "Chrome", "browserVersion": "91.0.4472.77", "screenWidthPoints": 939,
                       "screenHeightPoints": 937, "screenPixelDensity": 1, "screenDensityFloat": 1,
                       "utcOffsetMinutes": -240, "userInterfaceTheme": "USER_INTERFACE_THEME_LIGHT",
                       "mainAppWebInfo": {"graftUrl": "/results?search_query=light",
                                          "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                                          "isWebNativeShareAvailable": True}}, "user": {"lockedSafetyMode": False},
            "request": {"useSsl": True, "internalExperimentFlags": [], "consistencyTokenJars": []},
            "clickTracking": {"clickTrackingParams": "CBcQ7VAiEwiOkqzEsJnxAhXEYCoKHWj5Cfs="}, "adSignalsInfo": {
                "params": [{"key": "dt", "value": "1623737905524"}, {"key": "flash", "value": "0"},
                           {"key": "frm", "value": "0"}, {"key": "u_tz", "value": "-240"},
                           {"key": "u_his", "value": "4"}, {"key": "u_java", "value": "false"},
                           {"key": "u_h", "value": "1080"}, {"key": "u_w", "value": "1920"},
                           {"key": "u_ah", "value": "1040"}, {"key": "u_aw", "value": "1920"},
                           {"key": "u_cd", "value": "24"}, {"key": "u_nplug", "value": "3"},
                           {"key": "u_nmime", "value": "4"}, {"key": "bc", "value": "31"},
                           {"key": "bih", "value": "937"}, {"key": "biw", "value": "923"},
                           {"key": "brdim", "value": "0,0,0,0,1920,0,1920,1040,939,937"}, {"key": "vis", "value": "1"},
                           {"key": "wgl", "value": "true"}, {"key": "ca_type", "value": "image"}]}}, "query": "light",
                "webSearchboxStatsUrl": "/search?oq=light&gs_l=youtube.12...0.0.2.2902812.0.0.0.0.0.0.0.0..0.0....0...1ac..64.youtube..0.0.0....0.Ycsp_Yt-Q_g"}
        r = requests.post(url=self.__url, data=data, headers=self.__headers, proxies=self.__proxies)
        print(r.json())
