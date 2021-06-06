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
			"chat_id": 1234567898
		}
	],
	"bot_token": "telegram_bot_token"
}
```

Any number of users can be added under the `users` key. Each should contain the `name` of the user
