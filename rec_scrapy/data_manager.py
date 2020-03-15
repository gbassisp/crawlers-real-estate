# -*- coding: utf-8 -*-
import pymysql
import json
import datetime as dt
import random
import url_parser
import sqlalchemy
import os
from os.path import sep
import models
import config

class DataManager():
    """A custom MySQL managing module for all spiders"""
    current_urls = []
    loaded_urls = set() #set of URL loaded from database
    crawled_urls = set() #set of URL crawled on this session
    uncrawled_urls = set()
    obtained_crawling_urls = set() #set if URL obatined from parsing the crawled pages
    domains = []
    links = [] #list of dict with this structure: {'URLID': thisID, 'FullURL': link fetched from website, 'DomainID': domainID, 'DateIndexed': DateIndexed}
    session = None
    

    """dunder methods defined below"""
    def __init__(self, file_name=config.credentials_file, db_type=config.db_type, db_file=config.db_sqlite_file):
        '''Initialise loading and connecting to database'''        
        self.db_type = db_type
        self.file_name = file_name
        if not file_name:
            self.credentials = config.db_credentials
        else:
            self.credentials = self.load_credentials(file_name)
        self.session = self.connect_to_db()
        return
        
    def __enter__(self):
        """Establishes a connection; to be used with context manager"""
        return self #return THIS object with a connection established

    def __exit__(self, *args):
        """Finishes the connection; to be used with context manager"""
        self.session.commit()
        self.session.close() #closes the connection within this object
        print("Ended connection to the database")
    
    """Other methods"""
    
    '''SQLALCHEMY METHODS'''
    def create_engine(self):
        '''Create sqlalchemy database engine'''
        # sqlite://<nohostname>/<path>
        # mysql://user:password@host/db
        # create from current object parameters
        print('Creating database engine from parameters')
        if self.db_type == 'sqlite':
            print('Creating sqlite engine')
            engine = sqlalchemy.create_engine('{schema}://{hostname}/{db}'
            .format(schema = self.db_type, hostname = '', db = self.db_file), echo=False)
        elif self.db_type == 'mysql':
            print('Connecting to MySQL server')
            engine = sqlalchemy.create_engine(
                '{schema}+pymysql://{user}:{password}@{hostname}:{port}/{db}'
                    .format(schema = self.db_type, 
                        hostname = self.credentials['host'],
                        user = self.credentials['user'],
                        password = self.credentials['passwd'],
                        port = self.credentials['port'],
                        db = self.credentials['db']), 
                echo=False)
        else:
            # TODO: create engine for other database schemas
            print('Unable to create engine for db_type: {}'.format(self.db_type))
            raise
        print('Database engine created')
        return engine

    def connect_to_db(self):
        Session = sqlalchemy.orm.sessionmaker()
        engine = self.create_engine()
        print('Creating tables')
        models.Base.metadata.create_all(bind=engine)
        print('Connecting to database')
        #connection = engine.connect()
        print('Connection established')
        Session.configure(bind=engine)
        session = Session()
        self.session = session
        return session

     
    def set_save_file_settings(self, save_file=False, save_dir=''):
        pass
    
    def load_credentials(self, file_name):
        """Load the credentials from the json file"""
        with open(file_name,'r') as file:
                credentials = json.load(file)
        return credentials

    def set_domains(self, domains, domain_country):
        """Query the domain table to map current domains"""
        print('Querying domains')
        for domain in domains:
            current_domain, new = self.query(models.Domain, name=domain, country=domain_country)
            self.domains.append(current_domain)
        self.session.commit()
        return
    
    def query(self, model, defaults=None, **kwargs):
        '''Queries a class type in session and add it if it doesnt exists
        Returns the object from model'''
        new = False
        row = self.session.query(model).filter_by(**kwargs).first()
        if not row:
            new = True
            params = dict((k, v) for k, v in kwargs.items())
            params.update(defaults or {})
            row = model(**params)
            self.session.add(row)
        return row, new

        
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
        print(f'So far, {len(self.crawled_urls)} URLs have been crawled.')
        self.uncrawled_urls.discard(response_url)
        #TODO: save to database and return the ID
        return

    def save_new_urls(self, list_of_links):
        """Update the url table to add new urls"""
        now = dt.datetime.now()
        for url in list_of_links: # query each url
            for domain in self.domains: # each domain
                if domain.name in url: # verify if the url belongs to an allowed domain
                    current_link, new = self.query(models.Page, full_url=url, domain_id=domain.id, create_date=now)
        return

    def save_new_file(self, responseObj):
        pass
    
    

















































