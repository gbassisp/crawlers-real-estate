# -*- coding: utf-8 -*-
import scrapy


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    start_urls = ['http://zapimoveis.com.br/']

    def parse(self, response):
        pass
