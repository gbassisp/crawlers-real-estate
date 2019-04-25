# -*- coding: utf-8 -*-
import scrapy
import custom_spider_settings as unethical


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    start_urls = ['https://www.zapimoveis.com.br/'] #this shall be updated to start from previous session
    custom_settings = unethical.get_unethical_settings(name)	
    #load list of urls to crawl


    def parse(self, response):
        pass
