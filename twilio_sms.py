#!/usr/bin/python3
"""
A script to call the Twilio API for sending text messages
"""

import re
import os
import sys
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
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = '######################'
    auth_token = '######################'
    client = Client(account_sid, auth_token)
    phone_list = []

    cli = argparse.ArgumentParser(description="Send an SMS text using the Twilio API")
    cli.add_argument('-l', '--list', help="The phone number list can be a file (one per line) \
            or a list of phone numbers in quotes (must be space delimited, \
            phone numbers themselves cannot have spaces).")
    cli.add_argument('-b', '--body', help="The body of the message you want to send in quotes. \
            Max 160 characters.")
    #160_chars="---------------------------------------------------------------------------------------------------------------------------------------------------------------"
    opts = cli.parse_args(args)

    if len(sys.argv) == 1:
        cli.print_help()
        exit()

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

    #print(opts.body)
    #print(phone_list)
    #exit()

    confirm() # prompt for execution

    for phone_num in phone_list:
        phone_num = phone_num.replace(" ", "")
        if phone_num.startswith("1"): # if phone_num starts with 1 remove it
            phone_num = phone_num[1:]
        message = client.messages \
            .create(
                body=opts.body,
                from_='+1##########', # your twilio number - this costs about $1/month
                to='+1'+phone_num     # +1 is the USA country code
            )
        print("phone_num = {0} ; body = \"{1}\" ; {2}".format(phone_num, opts.body, message.sid))
        #exit()

if __name__ == '__main__':
    main(sys.argv[1:])
