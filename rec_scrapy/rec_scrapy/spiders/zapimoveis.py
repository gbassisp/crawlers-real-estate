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
    custom_settings = custom_spider_settings.get_unethical_settings(name)
    save_file = False #custom_spider_settings.save_file

    #load list of urls to crawl
    dm = data_manager.DataManager()
    id_allowed_domains = dm.load_domain_id(allowed_domains, domain_country)




    def parse(self, response):
        response_id = self.dm.save_new_response(response.url, response.status) #update the response table with the link and HTTP code
        parser_obj = url_parser.URLParser(response.url) #create a parser object for this response
        parser_obj.feed(response.body.decode('utf-8')) #feed the HTML to the parser
        new_links = list(set(parser_obj.output_list)) #this is smelly to me, but it works
        self.dm.save_new_urls(new_links) #update the url table with the urls retrieved from this page
        self.start_urls = self.dm.get_urls_to_crawl(self.start_urls) #updates the crawling queue
        
        #saving the HTML file
        if self.save_file:
            file_name = custom_spider_settings.save_dir + str(response_id) + '.html'
            with open(file_name, 'wb') as file:
                file.write(response.body)
