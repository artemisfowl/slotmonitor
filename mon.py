#!/usr/bin/env python

'''
	file: mon.py
	brief: Program to monitor the status of vaccination centers and notify the
	user

	author: sb
	date: Thu, 27 May 2021 19:55:16 +0530
	bugs: No known bugs
'''

# standard libs/modules
from logging import (info, debug)
from datetime import (datetime, timedelta)
from time import sleep

# custom libs/modules
from utils import (utl_pop_scode, utl_get_state_code, utl_read_config,
		utl_pop_dcode, utl_get_dist_code, utl_parse_args, utl_setup_logger,
		utl_get_availabilty_data, utl_parse_availability_data)
from utils import (SEARCH_WINDOW, DATE_FORMAT_DISTRICT_SEARCH)


def main() -> int:
	'''
		function: main
		brief: Execution entry point

		return: Returns 0 for success and -1 for failure
		date: Thu, 27 May 2021 19:56:15 +0530
		bugs: No known bugs
	'''

	utl_setup_logger(log=f"log_{datetime.now().date()}",
			is_debug_enabled=utl_parse_args())
	info(f"Starting monitoring application")
	scode_storage = utl_pop_scode()
	info("Populated state codes")

	dates = [datetime.today() + timedelta(days=x) for x in range(SEARCH_WINDOW)]
	dates = [x.strftime(DATE_FORMAT_DISTRICT_SEARCH) for x in dates]
	debug(f"Dates to be searched for : {dates}")


	info("Iterating through the users")
	while True:
		info("Reading the configuration file")
		confdata = utl_read_config('./config.json')
		debug(f"Configuration data read : {confdata}")
		debug(f"State codes and corresponding names : {scode_storage}")
		debug(f"Number of users : {len(confdata.users)}")
		process(confdata=confdata, scode_storage=scode_storage, dates=dates)
		sleep(120)

	return 0

def process(confdata: str, scode_storage: dict, dates: list):
	'''
		function: process
		brief: Function to start processing the availability data and send out
		the message

		param: confdata string containing the configuration data
		param: scode_storage dictionary containing the state name and
		corresponding state code
		param: dates list containing the dates in DD-MM-YYYY format for the
		search window
	'''

	info("Starting to fetch the information and send the message")
	debug(f"Bot token : {confdata.bot_token}")
	for user in confdata.users:
		debug(f"Name : {user.name}")
		debug(f"Desired Age Group : {user.age}")
		debug(f"Residing State : {user.state}")
		debug(f"Residing District : {user.district}")
		debug(f"Chat ID : {user.chat_id}")
		info(f"Getting residing state code for user : {user.name}")
		residing_state_code = utl_get_state_code(state_name=user.state,
				storage=scode_storage)
		debug(f"Residing state code : {residing_state_code}")
		residing_district_code = utl_get_dist_code(
				district_name=user.district,
				storage=utl_pop_dcode(district_code=residing_state_code))
		debug(f"Residing district code : {residing_district_code}")

		for date in dates:
			d = utl_get_availabilty_data(district_id=residing_district_code,
					date=date)
			info("About to parse the received availablility data")
			debug(f"Availability data serialized : {d}")
			utl_parse_availability_data(data=d, date=date, age=user.age,
					user_name=user.name, chat_id=user.chat_id,
					bot_token=confdata.bot_token)

if __name__ == '__main__':
	main()
