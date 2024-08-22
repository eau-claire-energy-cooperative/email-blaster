#!/usr/bin/env python3

import argparse
import datetime
import smtplib
import os
import yaml
from jinja2 import Environment, pass_context
from email.mime.text import MIMEText
from dotenv import load_dotenv

# load the env file (.env)
load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
SENDER = os.getenv("SENDER")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def get_date():
    """same as calling datetime.now()
    https://docs.python.org/3/library/datetime.html
    """
    return datetime.datetime.now()

def create_date(date_string, format):
    """same as calling strptime()
    https://docs.python.org/3/library/datetime.html
    """
    return datetime.strptime(date_string, format)

@pass_context
def lookup_email(ctx, items):
    """ returs value in dict where the key is an email
    used within templates as vars.map | lookup
    """

    if('email_address' in ctx.parent and ctx.parent['email_address'] in items):
        return items[ctx.parent['email_address']]
    else:
        return ''

def send_email(subject, body, sender, recipients):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL(HOST, PORT) as smtp_server:
       smtp_server.login(USERNAME, PASSWORD)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

# load command line arguments
parser = argparse.ArgumentParser(description='Email Blaster')
parser.add_argument('-f', '--file', required=True,
                    help='The path to the email template file to load')
parser.add_argument('-v', '--var', action='append',
                    help="Add a variable passed to templates in the form key=value")
parser.add_argument('-T', '--test', action='store_true',
                    help="Run in test mode (do not send messages)")

args = parser.parse_args()

# create the config and load jinja
config = None
jinja_env = Environment()
jinja_env.globals['current_date'] = get_date
jinja_env.globals['parse_date'] = create_date
jinja_env.filters['lookup_email'] = lookup_email

with open(args.file, 'r') as file:
    config = yaml.safe_load(file)

# set the mode
mode = 'bulk' if not 'mode' in config else config['mode']

# load custom template vars, if they exist
template_vars = config['template_vars'] if 'template_vars' in config else {}

# if cli vars are given add those too
if(args.var is not None):
    template_vars.update({s.split("=")[0]:s.split("=")[1] for s in args.var })

# render templates
subject = jinja_env.from_string(config['subject'])
message = jinja_env.from_string(config['message'])

print(f"Running in {mode} mode")
if(not args.test):
    if(mode == 'single'):
        for r in config['recipients']:
            send_email(subject.render(vars=template_vars, email_address=r),
                       message.render(vars=template_vars, email_address=r), SENDER, r)
    else:
        send_email(subject.render(vars=template_vars), message.render(vars=template_vars), SENDER, config['recipients'])
else:
    if(mode == 'single'):
        for r in config['recipients']:
            print(f"Recipient: {r}")
            print(f"Subject: { subject.render(vars=template_vars, email_address=r) }")
            print(f"Message: { message.render(vars=template_vars, email_address=r) }")
    else:
        print(f"Recipients: { config['recipients'] }")
        print(f"Subject: { subject.render(vars=template_vars) }")
        print(f"Message: { message.render(vars=template_vars) }")
