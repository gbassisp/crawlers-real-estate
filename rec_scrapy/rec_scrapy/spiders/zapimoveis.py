# -*- coding: utf-8 -*-
import scrapy
import custom_spider_settings
import data_manager #use this module to leave all connection handling out of the spider
import url_parser #this class should be used to retrieve the next crawling pages. It should be a very simple class
import config

class ZapimoveisSpider(scrapy.Spider):
    name = 'zapimoveis'
    handle_httpstatus_all = True
    allowed_domains = config.domains
    domain_country = "BRA" #3 letters only
    custom_settings, save_file, save_dir = custom_spider_settings.get_unethical_settings(name)
    
    
    def __init__(self):
        self.start_urls = [self.add_https_scheme(domain) for domain in self.allowed_domains]
        self.next_urls = set(self.start_urls)
        #Create data manager object
        dm = data_manager.DataManager('credentials.json')
        dm.set_save_file_settings(save_file, save_dir)
        dm.set_domains(allowed_domains, domain_country)

    def add_https_scheme(self, url):
        return 'https://{}'.format(url)
    
    def close(self, reason):
        self.dm.__exit__()
        super().close(self, reason)


    def parse(self, response):
        response_id = self.dm.save_new_response(response.url, response.status) #update the response table with the link and HTTP code
        self.next_urls.discard(response.url)
        try: #try parsing the page for new urls
            parser_obj = url_parser.URLParser(response.url) #create a parser object for this response
            parser_obj.feed(response.body.decode('utf-8')) #feed the HTML to the parser
            new_links = list(set(parser_obj.output_list)) #this is smelly to me, but it works
            self.dm.save_new_urls(new_links) #update the url table with the urls retrieved from this page
        except Exception as e:
            print('Could not parse the response, catched ', e)
        self.next_urls.update(self.dm.get_urls_to_crawl(list(self.next_urls))) #updates the crawling set
        self.dm.save_new_file(response)
        

        if self.next_urls is not None:
            next_page = self.next_urls.pop()
            print(f'There are {len(self.next_urls)} URLs remaining. Preparing to crawl {next_page}')
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
            #yield scrapy.Request(next(iter(self.next_urls)), callback=self.parse)
