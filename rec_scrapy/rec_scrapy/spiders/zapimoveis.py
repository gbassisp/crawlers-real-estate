# -*- coding: utf-8 -*-
import scrapy
import unethical


class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    start_urls = ['http://zapimoveis.com.br/']
    custom_settings = unethical.get_unethical_settings()	

    def parse(self, response):
        pass
