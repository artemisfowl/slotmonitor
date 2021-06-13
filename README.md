# slotmonitor
Cowin slot monitoring program for Covid Vaccination. The program does what it says, monitors the slots for a person for a specific state and district and sends out details of the same over Telegram.

## Setup steps
In order to setup this program, no extra libraries are required to be installed, unless the Python installation is having a minimal package list.

_Note_: It is better to create a Python virtual environment while setting this program up.

Steps:
1. [Optional] Create a Virtual Environment for Python 3.x
2. Clone this repository.
3. Create the Telegram bot
4. Edit and update the configuration file(config.json).
5. Run the program

## Configuration file details
The configuration file (config.json) present in the repository is read by the program in order to send the updates to the users.
A sample configuration is already present in the file and looks as follows:
```
{
	"users": [
		{
			"name" : "firstname-middlename-lastname",
			"age": 18,
			"state": "state as per Cowin portal",
			"district": "district as per Cowin portal",
			"enabled": true,
			"chat_id": 1234567898
		}
	],
	"bot_token": "telegram_bot_token"
}
```

Any number of users can be added under the `users` key. Each should contain the `name` of the user, the preferred `age` group or the age of the user itself,
the `state` as per the listing in Cowin portal, the `district` as per the Cowin portal and then the `chat_id` of the person with the Telegram bot. This can be
obtained by calling the `getUpdates` endpoint of the Telegram API.

`enabled` field, if set to true will allow for sending updates to the users, false will not allow for sending the messages to the users.

## Configuring the Telegram bot token
In order to obtain the telegram bot access token, one has to initiate a conversation with `@BotFather` on Telegram and issue the command `/newbot`. On doing so
and following the responses from `BotFather`, the telegram bot will be created. This access token needs to be provided in the configuration file for the
`bot_token` key.

## Running the program
In order to run the program in normal mode, just execute the file : `mon.py`. In order to debug the program run, execute the file with debug option : `mon.py -d` or
`mon.py --debug`. This will ensure debugging is enabled and the same can be seen in the log files.

_Note_: In the normal mode, the program logs INFO logs only; in DEBUG mode, the logging is extensive and uses a lot of space in HDD. If you are planning to set it
up on a server, please refrain from executing the program in DEBUG mode.
