# -*- coding: utf-8 -*-
import pymysql
import json
import datetime as dt
import random

class DataManager():
    """A custom MySQL managing module for all spiders"""
    file_name = 'credentials.json' #default file for this project
    credentials = {}
    current_urls = []
    loaded_urls = set() #set of URL loaded from database
    crawled_urls = set() #set of URL crawled on this session
    uncrawled_urls = set()
    obtained_crawling_urls = set() #set if URL obatined from parsing the crawled pages
    domains = []
    links = [] #list of dict with this structure: {'URLID': thisID, 'FullURL': link fetched from website, 'DomainID': domainID, 'DateIndexed': DateIndexed}
    connection = None

    def set_save_file_settings(self, save_file=False, save_dir=''):
        pass
    
    def load_credentials(self, file_name=file_name):
        """Load the credentials from the json file"""
        with open(file_name,'r') as file:
                credentials = json.load(file)
        return credentials

    def connect_to_database(self, credentials=credentials):
        """With the given credentials, establishes a connection with the database"""
        c = credentials
        return pymysql.connect(host=c['host'],user=c['user'],passwd=c['passwd'],port=c['port'], db=c['db'])

    def load_domain_id(self, domain_name, domain_country):
        """Query the domain table to get the DomainID for each domain in the list"""
        domain_id = []
        #connect to the database
        try:
            connected_manager = self
            cursorObject = connected_manager.connection.cursor()
            for domain in domain_name:
                selectQuery = f'SELECT DomainID FROM domain WHERE DomainName LIKE "%{domain}%" LIMIT 0, 1'
                insertQuery = f'INSERT INTO domain(DomainName, CountryName) VALUES ("{domain}", "{domain_country}")'
                #fetch the id
                cursorObject.execute(selectQuery)
                current_id = cursorObject.fetchall()
                #check if it is a new domain to the database
                if current_id == ():
                    #insert it to the database
                    cursorObject.execute(insertQuery)
                    #get the id which was generated by the server
                    cursorObject.execute(selectQuery)
                    current_id = cursorObject.fetchall()
                    connected_manager.connection.commit()
                domain_id.append(current_id[0][0])
                self.domains.append({'DomainID': current_id[0][0], 'DomainName': domain, 'CountryName': domain_country})
                self.load_new_urls_from_domain(current_id[0][0])
        except Exception as e:
            print("Could not load domain info, catched: ", e)
        return domain_id
        
    def get_urls_to_crawl(self, url_queue):
        """Append the new_urls to the current list and return a list respecting a minimum treshold"""
        if len(url_queue) < 50: #if list is big enough, don't change it
            if len(self.uncrawled_urls) < 100: #if it isn't, but we don't have much to provide, give what we've got
                for domain in self.domains:
                    self.load_new_urls_from_domain(domain["DomainID"])
                url_queue = list(set(url_queue).union(self.uncrawled_urls))
            else:
                url_queue = list(set(url_queue).union(set(list(self.uncrawled_urls)[:100])))
        print(f"Returning {len(url_queue)} URLs to crawl")
        return url_queue
    
    def load_new_urls_from_domain(self, domain_id):
        """Query the url and request tables to get non-crawled urls"""
        selectQuery = f'SELECT u.FullURL FROM url AS u WHERE u.DomainID = {domain_id} ORDER BY u.Priority DESC, RAND() LIMIT 50'
        try:
            connected_manager = self
            cursorObject = connected_manager.connection.cursor()
            cursorObject.execute(selectQuery)
            queryResults = cursorObject.fetchall()
            queryResults = [result[0] for result in queryResults]
            self.loaded_urls.update(queryResults)
            #TODO: query which urls have been crawled or not
            self.uncrawled_urls.update(set(queryResults) - self.crawled_urls)
            print(f"Fetched {len(queryResults)} new URLs from database. There are {len(self.uncrawled_urls)} waiting")
        except Exception as e:
            print("Could not load URLs to crawl, catched: ", e)
        return list(queryResults)

    def save_new_response(self, response_url, response_status):
        """Update the request table with current response"""
        self.crawled_urls.add(response_url)
        print(f'These URLs have been crawled: \n {self.crawled_urls}')
        self.uncrawled_urls.discard(response_url)
        #TODO: save to database and return the ID
        return

    def save_new_urls(self, list_of_links):
        """Update the url table to add new urls"""
        self.obtained_crawling_urls.update(list_of_links)
        now = dt.datetime.now()
        DateIndexed = now.strftime('%Y-%m-%d')
        current_urls = [url['FullURL'] for url in self.links]
        #connect to the database
        try:
            connected_manager = self
            cursorObject = connected_manager.connection.cursor()
            for link in list_of_links:
                for domain in self.domains:
                    if domain['DomainName'] in link:
                        if link not in current_urls:
                            domainID = domain['DomainID']
                            selectQuery = f'SELECT URLID FROM url WHERE FullURL LIKE "{link}" LIMIT 0, 1'
                            insertQuery = f'INSERT INTO url(FullURL, DomainID, DateIndexed) VALUES ("{link}", "{domainID}", "{DateIndexed}")'
                            #fetch the id
                            cursorObject.execute(selectQuery)
                            current_id = cursorObject.fetchall()
                            #check if it is a new url to the database
                            if current_id == ():
                                #insert it to the database
                                cursorObject.execute(insertQuery)
                                #get the id which was generated by the server
                                cursorObject.execute(selectQuery)
                                current_id = cursorObject.fetchall()
                                connected_manager.connection.commit()
                            self.links.append({'URLID': current_id[0][0], 'FullURL': link, 'DomainID': domainID, 'DateIndexed': DateIndexed})
        except Exception as e:
            print("Could not save new urls, catched: ", e)
        return

    def save_new_file(self, responseObj):
        pass
    
    """dunder methods defined below"""
    def __init__(self, file_name=file_name):
        '''Initialise loading and connecting to database'''
        arg = file_name
        try:
            self.file_name = arg
            self.credentials = self.load_credentials(arg)
            self.__enter__()
        except:
            print('WARNING: No such credentials')
            
    def __enter__(self):
        """Establishes a connection; to be used with context manager"""
        self.connection = self.connect_to_database(self.credentials)
        print("New connection to the database")
        return self #return THIS object with a connection established

    def __exit__(self, *args):
        """Finishes the connection; to be used with context manager"""
        self.connection.close() #closes the connection within this object
        print("Ended connection to the database")
            


















































