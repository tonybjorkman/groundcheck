from models import Instrument
from db import Session
import configparser
import os.path




class Settings():

	def __init__(self):
		self.config_file = 'real_config.ini'
		config = configparser.ConfigParser()
		if not os.path.exists(self.config_file):
			print('No config file found: using defult settings')
			self.create_test_config()
			self.config_file = 'default_config.ini'
		else:
			print('Config file found')
		
		
		config.read(self.config_file)


		#look at mail server use before finished
		self.server_address = config['Mail Settings']['Mail server address']
		self.server_user = config['Mail Settings']['Mail server user']
		self.server_pass = config['Mail Settings']['Mail server pass']
		
		#timings in hours
		self.time_to_test_first_time = float(config['Timed Events']['Initial time limit'])
		self.time_to_refresh = int(config['Timed Events']['Refresh interval'])
		self.time_to_update_database = int(config['Timed Events']['Database frequency'])

		self.instrument_list = self.list_instruments()
		self.import_instruments()

	


	#read instruments from config file
	def import_instruments(self):
		config = configparser.ConfigParser()
		config.read(self.config_file)

		#may change to match formatting of instruments in config file
		for instrument in config['Instruments']:
			#split string
			instr_list = config['Instruments'][instrument].split(", ")
			instr_name = instr_list[0]
			instr_descript = instr_list[1]
			instr_ip = instr_list[2]
			i = Instrument(name=instr_name, description=instr_descript, ip=instr_ip)
			Session.add(i)
			Session.commit()



	def get(self, category, param):
		parser = configparser.ConfigParser()
		parser.read(self.config_file)
		return parser[category][param]

	def list_instruments(self):
		parser = configparser.ConfigParser()
		parser.read(self.config_file)
		instrument_list = []
		for instrument in parser['Instruments']:
			instrument_list.append(instrument)
		return instrument_list

	#create test config file
	def create_test_config(self):
		config = configparser.ConfigParser()
		config['Mail Settings'] = {'Mail server address': 'address', 'Mail server user': 'user', 'Mail server pass': 'pass'}
		config['Instruments'] = {'Instrument 1': 'name1, descript1, ip1', 'Instrument 2': 'name2, descript2, ip2'}
		config['Timed Events'] = {'Initial time limit': '0.25', 'Refresh interval': '8', 'Database frequency': '24'}
		config['Key']={'Blowfish key': 'key'}
		with open('default_config.ini', 'w') as configfile:
			config.write(configfile)


#s=Settings()
#print(s.instrument_list)
#s.server_user='new user'
#print(s.server_user)