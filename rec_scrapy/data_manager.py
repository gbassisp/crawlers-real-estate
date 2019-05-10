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

	def load_new_urls_from_domain(self, domain_name):
		pass

	def save_new_response(self):
		pass

	"""all methods below are the __magic methods__"""
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
		