##########
twilio_sms
##########

A python program for accessing Twilio's API to send SMS messages.

Getting Started
---------------
You'll need a twilio account to use this script.  Sign up here:  https://www.twilio.com  
Once you have an account, grab your 'ACCOUNT SID' and 'AUTH TOKEN' from https://twilio.com/console 
and create a file named '.twilio_config' in the base of your cloned repo with the following format::

    account_sid=##########
    auth_token=###########
    twilio_num=###########
    country_code=1       # 1 is the USA country code, adjust for your location

Usage::

    twilio_sms.py [-h] [-l LIST] [-b BODY] [-v]
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LIST, --list LIST  The phone number list can be a file (one per line) or
                            a list of phone numbers in quotes (must be space
                            delimited, phone numbers themselves cannot have
                            spaces).
      -b BODY, --body BODY  The body of the message you want to send in quotes.
                            Max 160 characters.
      -v, --verbose         Print more verbose output.

Examples::

    twilio_sms.py -l phone_numbers.txt -b "Saturday at 9:30am.  Please come"
    twilio_sms.py -l '123-456-7890 987-654-3210' -b "The Party is on!" -v
