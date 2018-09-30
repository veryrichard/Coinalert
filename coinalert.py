"""
This script gets currency data from the coinmarketcap.com api.
It's a personal tool just to alert me when a coin reaches a particular price.

The original alert was just a simple windows sound and did not alert Mac users. However,
It has been modified to send email alerts using the core python email module and/or send SMS 
using the twilio API.
This is a very very simple *procedural* script. You and I know why I'm mentioning the obvious. If you dont, good.
"""
import time
import urllib.request
import urllib.parse
import json
print("""

""")
print("Welcome alert-seeking crypto human, I'm Zinny and I'll be taking your orders today.")
print("""


""")
print("How it works is I ask you for simple details, you fill them in correctly, and voila!")
print("""

""")
print("---"*30)
time.sleep(2)

def get_coin_details():
    """
    This function gets details of the coin from the user. The details required are 
    the name of the coin as it appears on CoinMarketCap; the currency to be checked, 
    whether BTC or USD and the future price to be alerted about.

    """
    coin_name = input("What is the name of the cryptocurrency as it appears on CoinMarketCap? For example, Savenode\n")
    coin_name = coin_name.lower()
    time.sleep(2)

    print("Do you wanna be alerted for the USD or BTC value? \n")
    currency = input("For BTC type 'BTC'; For USD type 'USD'. Leave out the single quotes.\n")
    currency = currency.lower()
    if currency == "btc":
        target_price = input("Enter your target price in BTC \n")
        target_price = float(target_price)
    elif currency == "usd":
        target_price = input("Enter your target price in USD \n")
        target_price = float(target_price)
    else:
        print("Incorrect value entered. Start again! \n")
        get_coin_details()

    return(coin_name, currency, target_price)


def get_coin_value():

    """
    This function queries the CoinMarketCap API using the supplied details from the get_coin_details() function.

    """
    # Unpack the tuple returned from the get_coin_details() call
    coin_name, currency, target_price = get_coin_details()

    #alert_list = [alert_type, phone_number, email_address]
   

    #get_alert_details()

    url = "https://api.coinmarketcap.com/v1/ticker/{}/".format(coin_name)

    # This block requests data from the API, writes it to a "coin_alert.txt" file 
    try:
        f = urllib.request.urlopen(url) 
        raw_data = f.read().decode("utf-8")
        with open("coin_alert.txt", "w") as file_obj:
            for data in raw_data:
                file_obj.write(raw_data)
                break #This makes the loop run only once. I only need one loop cycle to get the data I need
   
    except urllib.error.HTTPError:
        print(coin_name.title(), "is not yet listed on CoinMarketCap \n")
        try_new_coin = input("Try another coin? Yes or No \n")
        try_new_coin_list = ["yes", "yeah", "y", "ya", "yup", "yea", "yep", "ye"]
        if try_new_coin.lower() in try_new_coin_list:
            print("---"*30)
            get_coin_value() 
        else:
            exit()
    except urllib.error.URLError:
        print("Connection problems, please check your network \n") 
        try_new_coin = input("Try another coin? Yes or No \n")
        try_new_coin_list = ["yes", "yeah", "y", "ya", "yup", "yea", "yep", "ye"]
        if try_new_coin.lower() in try_new_coin_list:
            print("---"*30)
            get_coin_value() 
        else:
            exit()
    
    if alert_type == "sms":
        send_sms_alert("You have registered to get alerted when the price of {} hits {} {}".format(coin_name.title(), target_price, currency.upper()))
    elif alert_type == "email":
        send_email_alert("Coinalert Signup Confirmation", "You have registered to get alerted when the price of {} hits {} {}".format(coin_name.title(), target_price, currency.upper()) )
    elif alert_type == "both":
        send_email_alert("Coinalert Signup Confirmation", "You have registered to get alerted when the price of {} hits {} {}".format(coin_name.title(), target_price, currency.upper()) )
        send_sms_alert("You have registered to get alerted when the price of {} hits {} {}".format(coin_name.title(), target_price, currency.upper()))

    # This block opens and reads the data and wraps it in json format
    with open("coin_alert.txt", "r", encoding="utf-8") as json_data:
        json_coin_alert = json.load(json_data)

    if currency == "btc":
        current_price_btc = float((json_coin_alert[0]["price_btc"])) #The original data is in str format

        if current_price_btc < target_price:
            while current_price_btc < target_price:
                f = urllib.request.urlopen(url)
                raw_data = f.read().decode("utf-8")
                with open("coin_alert.txt", "w") as file_obj:
                    for data in raw_data:
                        file_obj.write(raw_data)
                        break

                with open("coin_alert.txt", "r", encoding="utf-8") as json_data:
                    json_coin_alert = json.load(json_data)
                    current_price_btc = float((json_coin_alert[0]["price_btc"])) #The original data is in str format
                if current_price_btc >= target_price:
                    alert_list = [alert_type, phone_number, email_address, email_password]
                    if alert_list[0] == "sms":
                        sms_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)
                        send_sms_alert(sms_message_body)
                    elif alert_list[0] == "email":
                        email_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                    else:
                        sms_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)
                        email_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                        send_sms_alert(sms_message_body)

                    break
                else:
                    print("Current price of {} is {}BTC, still hodl!".format(json_coin_alert[0]["name"],current_price_btc))
                    print("Next Price report in about 60 seconds.")
                    print("Loading next price...")

                
                time.sleep(60) #Wait for 60 seconds, the api rate limit 10 per minute however the endpoints 
                                #are updated every 5 mins, so waiting for 60 seconds is very okay.

        elif current_price_btc > target_price:
            while current_price_btc > target_price:
                f = urllib.request.urlopen(url)
                raw_data = f.read().decode("utf-8")
                with open("coin_alert.txt", "w") as file_obj:
                    for data in raw_data:
                        file_obj.write(raw_data)
                        break

                with open("coin_alert.txt", "r", encoding="utf-8") as json_data:
                    json_coin_alert = json.load(json_data)
                    current_price_btc = float((json_coin_alert[0]["price_btc"])) #The original data is in str format
                if current_price_btc <= target_price: # fire alert call
                    alert_list = [alert_type, phone_number, email_address, email_password]            
                    if alert_list[0] == "sms":
                        sms_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)
                        send_sms_alert(sms_message_body)
                    elif alert_list[0] == "email":
                        email_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                    else:
                        sms_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)
                        email_message_body = "{} has reached your target price of {} BTC".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                        send_sms_alert(sms_message_body)
                    break
                else:
                    print("Current price of {} is {}BTC, still hodl!".format(json_coin_alert[0]["name"],current_price_btc))
                    print("Next Price report in about 60 seconds.")
                    print("Loading next price...")

                time.sleep(60) 
            
        else:
            print("The current price is the same as your target price")
            get_coin_details()


    elif currency == "usd":
        current_price_usd = float((json_coin_alert[0]["price_usd"])) 

        if current_price_usd < target_price:
            while current_price_usd < target_price:
                f = urllib.request.urlopen(url)
                raw_data = f.read().decode("utf-8")
                with open("coin_alert.txt", "w") as file_obj:
                    for data in raw_data:
                        file_obj.write(raw_data)
                        break

                with open("coin_alert.txt", "r", encoding="utf-8") as json_data:
                    json_coin_alert = json.load(json_data)
                    current_price_usd = float((json_coin_alert[0]["price_usd"])) #The original data is in str format
                if current_price_usd >= target_price:
                    alert_list = [alert_type, phone_number, email_address, email_password]
                    if alert_list[0] == "sms":
                        sms_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)
                        send_sms_alert(sms_message_body)
                    elif alert_list[0] == "email":
                        email_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                    else:
                        sms_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)
                        email_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                        send_sms_alert(sms_message_body) #fire alert call
                    break
                else:
                    print("Current price of {} is ${}, still hodl!".format(json_coin_alert[0]["name"],current_price_usd))
                    print("Next Price report in about 60 seconds.")
                    print("Loading next price...")

                time.sleep(60) #Wait for 60 seconds, the api rate limit 10 per minute however the endpoints 
                                #are updated every 5 mins, so waiting for 60 seconds is very okay.

        elif current_price_usd > target_price:
            while current_price_usd > target_price:
                f = urllib.request.urlopen(url)
                raw_data = f.read().decode("utf-8")
                with open("coin_alert.txt", "w") as file_obj:
                    for data in raw_data:
                        file_obj.write(raw_data)
                        break

                with open("coin_alert.txt", "r", encoding="utf-8") as json_data:
                    json_coin_alert = json.load(json_data)
                    current_price_usd = float((json_coin_alert[0]["price_usd"])) #The original data is in str format
                if current_price_usd <= target_price:
                    alert_list = [alert_type, phone_number, email_address, email_password]
                    if alert_list[0] == "sms":
                        sms_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)
                        send_sms_alert(sms_message_body)
                    elif alert_list[0] == "email":
                        email_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                    else:
                        sms_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)
                        email_message_body = "{} has reached your target price of {} USD".format(coin_name.title(), target_price)       
                        send_email_alert("{} Price Alert".format(coin_name.title()), email_message_body)
                        send_sms_alert(sms_message_body)
                    break
                else:
                    print("Current price of {} is ${}, still hodl!".format(json_coin_alert[0]["name"],current_price_usd))
                    print("Next Price report in about 60 seconds.")
                    print("Loading next price...")

                time.sleep(60) 

        else:
            print("The current price is the same as your target price")
            get_coin_details()  

def send_email_alert(subject, message_body):
    """
    This function sends out an email once the user's target price is reached. Only Gmail addresses for now.
    More emails  will probably be supported in the future.

    """ 
    #return(alert_type, phone_number, email_address)
    #alert_type, phone_number, email_address = get_alert_details()

    #if alert_type == "email":
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    msg = MIMEMultipart()

    password = alert_list[3]
    msg['From'] = "Coinalert"
    msg['to'] = alert_list[2]
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(alert_list[2], password) #alert_list is the list that stores the alert type data
    
    server.sendmail(alert_list[2], alert_list[2], msg.as_string()) # The messages appear as messages you sent to yourself
    server.quit()


def send_sms_alert(sms_body):
    """
    This function is responsible for sending sms to users' mobile numbers once their chosen target price is reached or surpassed.
    The sms api is provided by Twilio and requires credentials, therefore users are advised to get their credentials for free
    at https://twilio.com after registering on the website. Note this supports only limited usage and once exhausted
    users have to pay.

    """
    from twilio.rest import Client


    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = alert_list[4]
    auth_token = alert_list[5]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                        body = sms_body,
                        from_ = alert_list[6],
                        to = alert_list[1])

    print(message.sid)
    print("SMS Sent Successfully!")




print("What type of alert do you prefer? Enter 'sms', 'email', or 'both' \n")
alert_type = input()
alert_type = alert_type.lower()

if alert_type == "sms":
    phone_number = input("Enter your phone number in international format. For instance, +15558675310 \n")
    twilio_account_sid = input("Enter your Twilio Account SID \n")
    twilio_auth_token = input("Enter your Twilio Auth Token \n")
    twilio_phone_number = input("Enter your Twilio phone number \n")
    email_address = False
    email_password = False
    alert_list = [alert_type, phone_number, email_address, email_password, twilio_account_sid, twilio_auth_token, twilio_phone_number]
elif alert_type == "email":
    print("For now only Gmail addresses are allowed.\n")
    email_address = input("Enter your Gmail address. For instance, earthling@gmail.com \n")
    email_password = input("Enter your Gmail address password. This is required to allow Python send a message using your account \n")
    phone_number = False
    twilio_account_sid = False
    twilio_auth_token = False
    twilio_phone_number = False
    alert_list = [alert_type, phone_number, email_address, email_password, twilio_account_sid, twilio_auth_token, twilio_phone_number]
elif alert_type == "both":
    print("For now only Gmail addresses are allowed.\n")
    email_address = input("Enter your Gmail address. For instance, earthling@gmail.com \n")
    email_password = input("Enter your Gmail address password. This is required to allow Python send a message using your account \n")
    phone_number = input("Enter your phone number in international format. For instance, +15558675310 \n")
    twilio_account_sid = input("Enter your Twilio Account SID \n")
    twilio_auth_token = input("Enter your Twilio Auth Token \n")
    twilio_phone_number = input("Enter your Twilio phone number \n")
    alert_list = [alert_type, phone_number, email_address, email_password, twilio_account_sid, twilio_auth_token, twilio_phone_number]
else:
    print("Incorrect value entered. Start again!")
    exit()


get_coin_value()
