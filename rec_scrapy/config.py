#generic config
db_type='mysql' #options are mysql or sqlite
db_sqlite_file=None #'zapimoveis.sqlite' # in case type is sqlite
zzz_on_error = 15 # sleep time for the service to restart used at the main function
zzz_ok = 45
domains = ['redentora.com.br', 'imobiliariafigueiredo.com.br', 'compactoimoveis.com.br', 'tebar.com.br', 'alfariopreto.com.br', 'imoteto.com.br', 'nadruz.com.br', 'rosanaimoveisriopreto.com.br', 'imobiliariamagnum.com.br', 'riopretoimobiliaria.com.br', 'procedenciaimoveis.com.br', 'mudriopreto.com.br', 'neroimoveis.com.br', 'nbiriopreto.com.br', 'capuanoimoveis.com.br', 'tessariimoveis.com.br', 'villariopreto.com.br']
# default credentials, 
# to be overriden by the credentials.py file
credentials_file=None #credentials.json
db_credentials={
    "host": "localhost", 
    "user": "root", 
    "passwd": "", 
    "port": 3306, 
    "db": "db-name"}

try:
    from credentials import *
except:
    print('No local credentials, using default')
