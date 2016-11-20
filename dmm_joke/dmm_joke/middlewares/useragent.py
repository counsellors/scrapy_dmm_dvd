# -*-coding:utf-8-*-  
  
  
"""避免被ban策略之一：使用useragent池。 
 
使用注意：需在settings.py中进行相应的设置。 
"""  
import logging
import random  
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware  
  
class RotateUserAgentMiddleware(UserAgentMiddleware):  
  
    def __init__(self, user_agent=''):  
        self.user_agent_list = user_agent  
  
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):  
        ua = random.choice(self.user_agent_list)  
        if ua:  
            #显示当前使用的useragent  
            print "********Current UserAgent:%s************" %ua  
  
            #记录  
            logging.info('Current UserAgent: '+ua)  
            request.headers.setdefault('User-Agent', ua)  
  