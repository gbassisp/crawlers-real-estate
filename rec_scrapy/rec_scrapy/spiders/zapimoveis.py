# -*- coding: utf-8 -*-
import scrapy
import custom_spider_settings as unethical
import data_manager #use this module to leave all connection handling out of the spider
import url_parser #this class should be used to retrieve the next crawling pages. It should be a very simple class

class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    domain_country = "Brazil"
    start_urls = ['https://www.zapimoveis.com.br/'] #this shall be updated to start from previous session
    custom_settings = unethical.get_unethical_settings(name)
    
    #load list of urls to crawl
    dm = data_manager.DataManager()
    id_allowed_domains = dm.get_domain_id(allowed_domains, domain_country)




    def parse(self, response):
        pass
