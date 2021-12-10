#!/usr/bin/env python3
import os
import binascii
from config import Config
import datetime
from twilio.rest import Client
import csv
import datetime
# What are the Possible SMS and MMS Message Statuses, and What do They Mean?
# https://support.twilio.com/hc/en-us/articles/223134347-What-are-the-Possible-SMS-and-MMS-Message-Statuses-and-What-do-They-Mean-

# Tracking the Delivery Status of an Outbound Twilio SMS or MMS Message
# https://support.twilio.com/hc/en-us/articles/360008989454-Tracking-the-Delivery-Status-of-an-Outbound-Twilio-SMS-or-MMS-Message


def log_message(message):
    with open(Config.LOG_FILE, "a") as fstream:
        print(Config.LOG_FILE)
        log_message = f"{str(message.date_created)} STATUS={message.status} SID={message.sid} " \
                      f"MESSAGE={message.body} MESSAGE_TO={message.to} MESSAGE_LENGHT={len(message.body)}\n"
        fstream.write(log_message)
        fstream.write("\n")


def send_message(to_send_number, body_message):

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print("body_message", body_message)
    # Your Account SID from twilio.com/console
    account_sid = Config.TWILLIO_SID
    # Your Auth Token from twilio.com/console
    auth_token = Config.TWILLIO_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_send_number,
        messaging_service_sid=Config.MESSAGING_NM,
        body=body_message)



    # MONITOR STATUS OF YOUR MESSAGE
    # https://www.twilio.com/docs/sms/send-messages#monitor-the-status-of-your-message

    # Troubleshooting Undelivered Twilio SMS Messages
    # https://support.twilio.com/hc/en-us/articles/223181868-Troubleshooting-Undelivered-Twilio-SMS-Messages
    return message


def run_send_a_message(data):
    # E.G. data : [('Hallo johny, Black friday fever at !Thanks!',
    #               '+351913432442',
    #               41,
    #               1)]

    # TODO:
    #  if we need to verify and alert user that messages were sent
    sent_messages_list = [] # a list with messages.sid sent
    # LOGGING BLOCK
    for row in data:
        message = send_message(to_send_number=row[1], body_message=row[0])
        print("message: ", message)
        print("message sid", message.sid)
        log_message(message)
        sent_messages_list.append(message.sid)


if __name__ == '__main__':
    #run_send_A_message()
    pass

