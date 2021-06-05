'''
	file: utils.py
	brief: File containing the utility functions

	author: sb
	date: Thu, 27 May 2021 20:03:07 +0530
	bugs: No known bugs
'''

# standard libs/modules
from requests import get
from json import (loads, dumps, load)
from types import SimpleNamespace
from typing import Union
from argparse import ArgumentParser
from logging import (getLogger, StreamHandler, FileHandler, Formatter,
		basicConfig, info, debug, error)
from logging import (DEBUG, INFO)
from sys import stdout
from urllib import parse

# constants section
BASE_URL = "https://cdn-api.co-vin.in/api/v2/"
STATES_ENDPOINT = "admin/location/states"
DISTRICTS_ENDPOINT = "admin/location/districts/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)' \
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102' \
		'Safari/537.36'}
AVAILABILITY_ENDPOINT = "appointment/sessions/public/" \
		"calendarByDistrict?district_id={}&date={}"
SEARCH_WINDOW = 14
DATE_FORMAT_DISTRICT_SEARCH = "%d-%m-%Y"

# telegram constants section
TAPI_BASE_URL = "https://api.telegram.org/bot{}{}"
TAPI_UPDATES_ENDPOINT = "/getUpdates"
TAPI_SEND_MSG_ENDPOINT = "/sendMessage?chat_id={}&text={}"

def utl_telegram_send_message(
		message: str, chat_id: str, bot_token: str) -> int:
	'''
		function: utl_telegram_send_message
		brief: Function to send message from the telegram bot

		param: message string containing the message text
		param: chat_id string containing the id of the chat to be
		responded to
		param: bot_token string containing the Telegram bot authentication
		token

		date: Wed, 02 Jun 2021 11:41:15 +0530
		bugs: No known bugs
	'''

	info("Sending message to Receipient")
	url = TAPI_BASE_URL.format(bot_token, TAPI_SEND_MSG_ENDPOINT)
	url = url.format(chat_id,
			parse.quote_plus(message))
	debug(f"Final URL : {url}")

	response = get(url=url, headers=HEADERS)
	debug(f"Response status of send message call : {response.status_code}")

	return 0

def utl_pop_scode() -> Union[dict,None]:
	'''
		function: utl_pop_scode
		brief: Function to create a dictionary of state codes and state names

		return: Returns a dictionary of state name: state code, else None
		dictionary
		date: Thu, 27 May 2021 20:06:04 +0530
		bugs: No known bugs
	'''

	info("Getting state codes")
	r = None
	debug(f"Hitting URL : {BASE_URL}{STATES_ENDPOINT}")
	response = get(url=f"{BASE_URL}{STATES_ENDPOINT}", headers=HEADERS)
	debug(f"Response status code : {response.status_code}")
	debug(f"Response JSON : {response.json()}")

	if response.status_code == 200:
		debug("Serializing the JSON data")
		r = utl_objectify(data=response.json())
		debug(f"Serialized output : {r}")
		r = {state.state_name.lower(): state.state_id for state in r.states}
		debug(f"Finalized dictionary : {r}")

	return r

def utl_pop_dcode(district_code: int) -> Union[dict,None]:
	'''
		function: utl_pop_dcode
		brief: Function to fetch the districts of a specific state

		param: district_code is an integer containing the state code of the
		user's residing state
		return: Returns a dictionary containing district name : district id or
		None

		date: Thu, 27 May 2021 21:49:05 +0530
		bugs: No known bugs
	'''

	info("Started populating the district codes")
	if district_code < 0 or not isinstance(district_code, int):
		return None

	r = None
	debug(f"Hitting URL : {BASE_URL}{DISTRICTS_ENDPOINT}{district_code}")
	response = get(url=f"{BASE_URL}{DISTRICTS_ENDPOINT}{district_code}",
			headers=HEADERS)
	debug(f"Response status code : {response.status_code}")
	debug(f"Response JSON data : {response.json()}")

	if response.status_code == 200:
		debug("Serializing reponse JSON data")
		r = utl_objectify(data=response.json())
		debug(f"Serialized district data : {r}")
		r = {d.district_name.lower(): d.district_id for d in r.districts}
		debug(f"Finalized district data : {r}")

	return r

def utl_objectify(data: dict) -> SimpleNamespace:
	'''
		function: objectify
		brief: Function to conver the provided json data to object

		param: data is a dictionary which contains the response JSON
		return: Returns a SimpleNamespace object

		date:Thu, 27 May 2021 20:31:49 +0530
		bugs: No known bugs
	'''

	return loads(dumps(data), object_hook=lambda s: SimpleNamespace(**s))

def utl_get_state_code(state_name: str, storage: dict) -> Union[int,None]:
	'''
		function: utl_get_state_code
		brief: Function to return the state code for the specified state name

		param: state_name is a string containing the name of the state
		param: storage is the dictionary which contains the state name: state
		code
		return: Returns the state code if present else returns None

		date: Thu, 27 May 2021 20:39:25 +0530
		bugs: No known bugs
	'''

	if storage is None or not isinstance(storage, dict):
		return None

	if state_name is None or not isinstance(state_name, str):
		return None

	return storage.get(state_name.lower())

def utl_get_dist_code(district_name: str, storage: dict) -> Union[int,None]:
	'''
		function: utl_get_dist_code
		brief: Function to return the district code for the specified district
		name

		param: district_name is a string containing the name of the district
		param: storage is the dictionary which contains the state name: state
		code
		return: Returns the district code if present else returns None

		date: Thu, 27 May 2021 21:51:02 +0530
		bugs: No known bugs
	'''

	if storage is None or not isinstance(storage, dict):
		return None

	if district_name is None or not isinstance(district_name, str):
		return None

	return storage.get(district_name.lower())

def utl_get_availabilty_data(district_id: int, date: str) -> \
		Union[SimpleNamespace, None]:
	'''
		function: utl_get_availabilty_data
		brief: Function to hit the final url and return the serialized data

		param: district_id integer containing the preferred district code
		param: dat string containing the date in DD-MM-YYYY format
		return: Returns a SimpleNamespace containing the JSON data or None

		date: Tue, 01 Jun 2021 01:59:15 +0530
		bugs: No known bugs
	'''

	info("Getting the availabilty data")

	if district_id is None or not isinstance(district_id, int):
		error(f"District ID : {district_id} should be an integer")
		return None
	if date is None or not isinstance(date, str) or len(date) == 0:
		error(f"Date : {date} should be an string in DD-MM-YYYY format")
		return None

	debug(f"District id provided : {district_id}")
	debug(f"Date provided : {date}")

	r = None

	url = f"{BASE_URL}{AVAILABILITY_ENDPOINT}"
	url = url.format(district_id, date)
	debug(f"Final endpoint : {url}")

	r = get(url=url, headers=HEADERS)
	if r.status_code == 200:
		r = utl_objectify(data=r.json())

	return r

def utl_parse_availability_data(data: SimpleNamespace, date: str, age: int,
		user_name: str, chat_id: int, bot_token: str):
	'''
		function: utl_parse_availability_data
		brief: Function to parse the availability data

		param: data a SimpleNamespace containing the serialized response JSON
		param: date string containing date in DD-MM-YYYY format
		param: age integer contain
		param: user_name string containing the full name of the user
		param: chat_id integer containing the id of the chat to which the
		message needs to be sent
		param: bot_token string containing the authentication key for the
		telegram bot

		date: Wed, 02 Jun 2021 20:18:10 +0530
		bugs: No known bugs
	'''

	info("Starting to parse the availability data")

	if data is None or not isinstance(data, SimpleNamespace):
		error("Data provided is not consistent, please check data")
	if date is None or not isinstance(date, str) or len(date) == 0:
		error("Date should be in DD-MM-YYYY format")
	if age is None or not isinstance(age, int):
		error("Age needs to be a proper number")
	if user_name is None or not isinstance(user_name, str) or \
			len(user_name) == 0:
		error("User full name needs to be provided")

	debug(f"Data received : {data}")
	debug(f"Chat ID for {user_name} : {chat_id}")

	if data.centers:
		info(f"Date: {date}")
		for center in data.centers:
			for session in center.sessions:
				if session.min_age_limit <= age:
					capacity = int(session.available_capacity)
					if capacity > 0:
						message = f"Available on : {date}"
						message += f"\n\nCenter : {center.name}"
						message += f"\n\nBlock Name : {center.block_name}"
						message += f"\n\nPrice : {center.fee_type}"
						message += f"\n\nAvailble capacity: {capacity}"
						if session.vaccine != '':
							message += f"\n\nVaccine name : {session.vaccine}"

						info(f"Message to be sent : {message}")
						utl_telegram_send_message(
								message=message, chat_id=chat_id,
								bot_token=bot_token)
					else:
						message = f"Capacity for {center.name} "
						message += f"completely utilized for date : {date}"
						info(message)
	else:
		info(f"No available slots on : {date}")

def utl_read_config(configpath: str) -> Union[SimpleNamespace,None]:
	'''
		function: utl_read_config
		brief: Function to read the configuration file and return the data as a
		dictionary

		param: configpath string containing the configuration file path
		return: Returns SimpleNamespace or None

		date: Thu, 27 May 2021 20:57:43 +0530
		bugs: No known bugs
	'''

	info("Reading the configuration file")
	if configpath is None or not isinstance(configpath, str):
		return None

	r = None
	debug(f"Configuration file path provided : {configpath}")
	with open(configpath) as f:
		r = load(f)
	debug(f"Configuration read from file : {r}")

	return utl_objectify(data=r)

def utl_parse_args() -> bool:
	'''
		function: utl_parse_args
		brief: Function to parse the arguments

		return: returns true if -d or --debug provided in CLI arguments, else
		False. False means Info mode and True means Debug mode
		date: Sat, 29 May 2021 19:48:59 +0530
		bugs: No known bugs
	'''

	p = ArgumentParser(prog="mon",
			description="Program to monitor and notify about available " \
				"vaccination slots")
	p.add_argument("-d", "--debug", action="store_true",
			help="Optional argument, enable debug mode")

	args = p.parse_args()

	return args.debug

def utl_setup_logger(log: str, is_debug_enabled: bool = False,
		log_to_file: bool = True, log_to_stdio: bool = False):
	'''
		function: utl_setup_logger
		brief: Function to set up the logger for the program

		param: log string containing the log file directory path along with
		the log file name
		param: is_debug_enabled is a boolean set to False by default
		param: log_to_file boolean flag, by default set to True.
		Set flag to false in order to stop logging to file
		param: log_to_stdio boolean flag, default set to False. Set true in
		order to log to stdio
	'''

	log_fmt = Formatter("%(asctime)s : <%(threadName)-12.12s>" +
			"(%(levelname)-5.5s) " +
			"-: %(filename)s:%(lineno)s - %(funcName)s() :-" +
			" %(message)s")
	root_logger = getLogger()
	fhandler = None	# file handler - writes to the file
	chandler = None # console handler - writes to the stdio

	# setting up the file handler
	fhandler = FileHandler(log)
	fhandler.setFormatter(log_fmt)

	# setting up the console handler
	chandler = StreamHandler()
	chandler.setFormatter(log_fmt)

	if log_to_file:
		root_logger.addHandler(fhandler)
	if log_to_stdio:
		root_logger.addHandler(chandler)

	if is_debug_enabled:
		root_logger.setLevel(DEBUG)
	else:
		root_logger.setLevel(INFO)
