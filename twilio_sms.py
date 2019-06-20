#!/usr/bin/python3
"""
A script to call the Twilio API for sending text messages
"""

import re
import os
import sys
import logging
import argparse

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

def confirm():
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """

    answer = ""
    while answer not in ["y", "n"]:
        answer = input("\nAre you sure you want to send the SMS message(s)? [Y/n] ").lower()

    if answer == "n":
        exit("Exiting.")
    return True

def main(args):
    """
    This script is meant to be run from the cli
    """
    # Get twilio account and auth info from config file
    file_name = '.twilio_config'
    account_sid = ''
    auth_token = ''
    phone_list = []

    if not os.path.exists(file_name):
        print('{} file not found! Exiting.'.format(file_name))
        exit(2)

    with open(file_name) as read_file:
        lines = read_file.read().strip().split('\n')

    for line in lines:
        if 'account_sid' in line:
            pieces = line.split('=')
            account_sid = pieces[1]

        if 'auth_token' in line:
            pieces = line.split('=')
            auth_token = pieces[1]

    client = Client(account_sid, auth_token)

    logging.basicConfig(filename='twilio_sms.log', filemode='a',\
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
            datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    cli = argparse.ArgumentParser(description="Send an SMS text using the Twilio API")
    cli.add_argument('-l', '--list', help="The phone number list can be a file (one per line) \
            or a list of phone numbers in quotes (must be space delimited, \
            phone numbers themselves cannot have spaces).")
    cli.add_argument('-b', '--body', help="The body of the message you want to send in quotes. \
            Max 160 characters.")
    cli.add_argument('-v', '--verbose', action="store_true", help="Print more verbose output.")
    opts = cli.parse_args(args)

    if len(sys.argv) == 1:
        cli.print_help()
        exit()

    if len(opts.body) > 160:
        print("\nYour message is {0} characters, the max is 160, please fix.\
                \nExiting.".format(len(opts.body)))
        exit(2)

    if os.path.isfile(opts.list):
        with open(opts.list) as phone_file:
            for line in phone_file:
                #print("line = {0}".format(line))
                line = line.split('#', 1)[0]
                line = re.sub('[-().+]', '', line)
                if line:
                    phone_list.append(line.strip())
    else:
        line = re.sub('[-().+]', '', opts.list)
        phone_list = line.split(' ')

    phone_list = list(filter(None, phone_list))

    if opts.verbose:
        print('\nMessage:')
        print(opts.body)
        print('\nPhone List:')
        print(phone_list)

    #exit()

    confirm() # prompt for execution
    print('')

    for phone_num in phone_list:
        phone_num = phone_num.replace(" ", "")
        if phone_num.startswith("1"): # if phone_num starts with 1 remove it
            phone_num = phone_num[1:]
        message = client.messages \
            .create(
                body=opts.body,
                from_='+13853360208', # your twilio number, costs about $1/month, each SMS $0.0075
                to='+1'+phone_num     # +1 is the USA country code
            )
        logging.info("phone_num = %s ; body = \"%s\" ; %s", phone_num, opts.body, message.sid)
        if opts.verbose:
            print("phone_num = {0} ; body = \"{1}\" ; {2}".format(phone_num, opts.body, message.sid))

        #exit()

    print("Done.")

if __name__ == '__main__':
    main(sys.argv[1:])
