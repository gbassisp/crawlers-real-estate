#This file is intended to override crawling settings on a basic scrapy spider
#The main goal is to keep the settings.py file simple and fitting most spider needs, so only the exceptions should import this
import os
#values to be overriden on the settings.py file are this:


def get_unethical_settings(name_of_the_spider=''):
	#ZapImoveis profile (unethical and "untraceable")	
	if name_of_the_spider == 'zapimoveis':
		BOT_NAME = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
		ROBOTSTXT_OBEY = False
		DOWNLOAD_DELAY = 40 #those bastards won't allow webscraping
		COOKIES_ENABLED = True #I'm not sure this is necessary, but just in case
		save_file = True
		save_directory = os.curdir + '\\html-files\\'
		return {'BOT_NAME':BOT_NAME, 'ROBOTSTXT_OBEY':ROBOTSTXT_OBEY,'DOWNLOAD_DELAY':DOWNLOAD_DELAY,'COOKIES_ENABLED':COOKIES_ENABLED}, save_file, save_directory
	

	#for any other profile, return an empty dictionary
	return {}

	

def get_standard_settings():
        BOT_NAME = 'rec_scrapy (+http://www.yourdomain.com)'
        ROBOTSTXT_OBEY = True
        DOWNLOAD_DELAY = 1
        COOKIES_ENABLED = True
        return {'BOT_NAME':BOT_NAME, 'ROBOTSTXT_OBEY':ROBOTSTXT_OBEY,'DOWNLOAD_DELAY':DOWNLOAD_DELAY,'COOKIES_ENABLED':COOKIES_ENABLED}

