"""
入口
"""
from spider import YSpider

SEARCH_KEYWORD = 'light'


def main():
    ys = YSpider(SEARCH_KEYWORD)
    ys.run()


if __name__ == '__main__':
    main()
