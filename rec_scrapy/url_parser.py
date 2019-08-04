#This is a simple class to parse the html file and retrieve relevant URLs
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import re

class URLParser(HTMLParser):
    '''Parses the HTML body to retrieve URL on <a href=""> tags'''
    #Regular expression for checking for relative URLs
    relative_url_regex = re.compile(r'/^[^\/]+\/[^\/].*$|^\/[^\/].*$/gmi')
    def __init__(self, cur_url, url_input=None):
        HTMLParser.__init__(self)
        if url_input is None:
            self.output_list = []
        else:
            self.output_list = url_input
        self.cur_url = cur_url
        self.domain = urlparse(cur_url).netloc

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            #converts relative to absolute url before appending to the output list
            absolute_url = urljoin(self.cur_url, dict(attrs).get('href'))
            self.output_list.append(absolute_url) if self.check_domain(domain=self.domain,url=absolute_url) else None
    
    def check_domain(self, domain, url):
        if domain in urlparse(url).netloc:
            return True
        else:
            return False