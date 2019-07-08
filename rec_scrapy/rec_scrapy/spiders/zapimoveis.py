# -*- coding: utf-8 -*-
import scrapy
import custom_spider_settings
import data_manager #use this module to leave all connection handling out of the spider
import url_parser #this class should be used to retrieve the next crawling pages. It should be a very simple class

class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    allowed_domains = ['zapimoveis.com.br']
    domain_country = "Brazil"
    start_urls = ['https://www.zapimoveis.com.br/'] #this shall be updated to start from previous session
    next_urls = set(start_urls)
    custom_settings, save_file, save_dir = custom_spider_settings.get_unethical_settings(name)
    
    #Create data manager object
    dm = data_manager.DataManager('credentials.json')
    dm.set_save_file_settings(save_file, save_dir)
    dm.load_domain_id(allowed_domains, domain_country)




    def parse(self, response):
        response_id = self.dm.save_new_response(response.url, response.status) #update the response table with the link and HTTP code
        parser_obj = url_parser.URLParser(response.url) #create a parser object for this response
        parser_obj.feed(response.body.decode('utf-8')) #feed the HTML to the parser
        new_links = list(set(parser_obj.output_list)) #this is smelly to me, but it works
        self.dm.save_new_urls(new_links) #update the url table with the urls retrieved from this page
        self.next_urls.update(self.dm.get_urls_to_crawl(list(self.next_urls))) #updates the crawling set
        self.dm.save_new_file(response)

        if self.next_urls is not None:
            next_page = self.next_urls.pop()
            print(f'preparing to crawl {next_page}')
            yield scrapy.Request(next_page, callback=self.parse)
