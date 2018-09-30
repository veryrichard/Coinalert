# Coinalert
Cryptocurrency price alert that supports email and sms alerts.

This is a simple Python script that is run from the terminal.
The script runs until the set price is attained, at which point an email and/or SMS is sent to a dedicated email address/phone number.

The script depends on the Twilio Python library for the SMS function, and it will definitely fail without it should you choose to receive SMS alerts. The SMS function assumes you have an account with Twilio and your account has some credit. Every new Twilio account is provided with about $15 in free credits for testing. If you would like to utilize the SMS function then sign up for a Twilio account, verify your number since the free account only allows sending sms to a verified number. Also you may be required to "verify" your country as well.
For the email function, you need a Gmail account and will also need to "allow less secured apps" from your Gmail settings. Please google how to do that.

This software sends alerts and nothing more. It also does that with your internet connection and needs to keep running on either your local computer or vps server. Please do not base financial decisions on the reports of this software. For instance, you may run it on your server and go to bed hoping it will alert you, however, the program may have stopped for some reason. So please use your discretion if you'll ever use this software

# Dependencies
1. Python 3: Usually installed on Linux systems. If not installed, then install for your particular operating system.

2. PIP: Package manager for Python. You need this to install the Twilio library

3. Twilio: This is required for SMS alerts. If you dont need SMS alerts then you only need the Python interpreter to run this script.


# This is dedicated to the Savenode community (https://savenode.io)
