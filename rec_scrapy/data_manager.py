# -*- coding: utf-8 -*-
import pymysql
import json

class DataManager():
	"""A custom MySQL managing module for all spiders"""
	file_name = 'credentials.json' #default file for this project
	credentials = {}
	connection = None

	def load_credentials(self, file_name=file_name):
		"""Load the credentials from the json file"""
		with open(file_name,'r') as file:
			credentials = json.load(file)
		return credentials

	def connect_to_database(self, credentials=credentials):
		"""With the given credentials, establishes a connection with the database"""
		c = credentials
		return pymysql.connect(host=c['host'],user=c['user'],passwd=c['passwd'],port=c['port'], db=c['db'])

	def get_domain_id(self, domain_name, domain_country):
		self.domains = {}
		domain_id = []
		#connect to the database
		with DataManager(self.file_name) as connected_manager:
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
					print("Domain not found in the database")
					cursorObject.execute(insertQuery)
					print("Domain added to the database")
					cursorObject.execute(selectQuery)
					current_id = cursorObject.fetchall()
					connected_manager.connection.commit()
				domain_id.append(current_id[0][0])
		return domain_id

	def load_new_urls_from_domain(self, domain_id):
		pass

	def save_new_response(self):
		pass

	"""dunder methods defined below"""
	def __init__(self, file_name=file_name):
		'''Initialise loading and connecting to database'''
		arg = file_name
		try:
			self.file_name = arg
			self.credentials = self.load_credentials(arg)
		except:
			print('WARNING: No such credentials')
		
	def __enter__(self):
		"""Establishes a connection; to be used with context manager"""
		self.connection = self.connect_to_database(self.credentials)
		return self #return THIS object with a connection established

	def __exit__(self, *args):
		"""Finishes the connection; to be used with context manager"""
		self.connection.close() #closes the connection within this object
		