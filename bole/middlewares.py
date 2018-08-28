import json
import random
from fake_useragent import UserAgent
from selenium import webdriver
import time
from bole.utils import proxies_utils

from scrapy.downloadermiddlewares.retry import RetryMiddleware


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self,crawler):
        super(RandomUserAgentMiddlware, self).__init__()#super的作用是获取父类的初始方法，这里是获取一个类方法
        self.ua = UserAgent()#这里是引进的一个随机UA的模块
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)#获取crawler，其中包括setting

    def process_request(self, request, spider):
        # print(request.headers)
        def get_ua():
            return getattr(self.ua, self.ua_type)#getattr函数可以根据传递的后边参数的不同，获取前边函数的不同值方法，类似与'.'
        random_ua = get_ua()
        request.headers.setdefault('User_Agent', random_ua)


class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        while True:
            try:
                with open(r'E:\lyh\ditu\tianji\bole-master\bole\utils\proxies.txt', 'r') as f:
                    proxies = f.readlines()
                proxy = random.choice(proxies)
                request.meta["proxy"] = proxy
                break
            except Exception as e:
                print(e)
                time.sleep(1)
                continue






