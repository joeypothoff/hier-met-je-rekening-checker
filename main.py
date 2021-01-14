import os
import smtplib
import ssl

from dotenv import load_dotenv
from tweepy import OAuthHandler, StreamListener, Stream

# load dotenv so env variables can be used
load_dotenv()

# twitter credentials
auth = OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "SENDER_EMAIL_HERE"
receiver_email = "RECEIVER_EMAIL_HERE"
password = input("Vul je wachtwoord in: ")
message = """\
Subject: Naam genoemd

Je naam is genoemd op radio 538. Bel nu binnen 15 minuten!.
"""

# class to send email when name is being called
class StdOutListener(StreamListener):

    # receive all messages
    def on_data(self, data):
        # search criteria
        search = "NAAM_HIER"

        # if criteria is found
        if search in data:
            # send mail to receiver
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)

        return True

    # if error occurs
    def on_error(self, status):
        print(status)

# if script is running
if __name__ == '__main__':
    listener = StdOutListener()

    # initiate stream
    stream = Stream(auth, listener)
    stream.filter(follow=['1334169320407126020'])  # @HMJRK on twitter
