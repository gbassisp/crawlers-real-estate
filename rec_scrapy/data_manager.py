# -*- coding: utf-8 -*-
import pymysql
import json

class DataManager():
	"""A custom MySQL managing module for all spiders"""
	file_name = 'credentials.json'
	credentials = {}

	def load_credentials(self, file_name=file_name):
		with open(file_name,'r') as file:
			credentials = json.load(file)
		return credentials

	def connect_to_database(self, credentials=credentials):
		c = credentials
		return pymysql.connect(host=c['host'],user=c['user'],passwd=c['passwd'],port=c['port'], db=c['db'])

	def load_new_urls_from_domain(self, domain_name):
		pass

	def save_new_response(self):
		pass

	def __init__(self, file_name=file_name):
		#super(DataManager,	self).__init__()
		arg = file_name
		self.file_name = arg
		self.credentials = self.load_credentials(arg)

