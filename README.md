# Email Blaster
[![License](https://img.shields.io/github/license/eau-claire-energy-cooperative/email-blaster)](https://github.com/eau-claire-energy-cooperative/email-blaster/blob/main/LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

Sometimes you just have to blast out some emails. This is a rather simple Python script to pull in some email template files and send them through your configured SMTP service. Works with a public service like Gmail or your own SMTP. This is useful if you have emails that need to go out on a timer or perhaps have some dynamic content you want to set per message as they're sent.

Message files are configured using YAML and can contain [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/templates/) to insert dynamic content.

## Table Of Contents

- [Install](#install)
- [Usage](#usage)
  - [Setup][#setup]
  - [Running][#running]
  - [Google SMTP Relay][#google-smtp-relay]
- [Templating][#templating]
  - [Templates In Single Mode][#templates-in-single-mode]
- [License][#license]

## Install

This script is installing using a Python [virtual environment](https://docs.python.org/3/library/venv.html) so keep everything as simple as possible. This was tested on a Linux system but would probably work on Windows as long as the requirements are met.

```
# install os deps
sudo apt-get install git python3-pip python3-venv

# clone the repo
git clone https://github.com/eau-claire-energy-cooperative/email-blaster

# create the virtual environment
cd email-blaster
python3 -m venv .venv
source .venv/bin/activate

# install python requirements
pip3 install -r requirements.txt

# deactivate virtual environment when done
deactivate

```

## Usage


### Setup

To use the email blaster first a few things need to be setup.

1. Copy the env-sample file as `.env` and set your outgoing SMTP server information.
2. Copy the sample email message file in the `messages` folder to `messages/example-message.yaml`

Edit the example message YAML file to create your own test message. The keys are fairly self explanatory but are:

* mode _(optional)_ - the email mode to use, valid options are `bulk` or `single`. Bulk mode sends all at once and is the default. Single sends one at a time ([see below](#templates-in-single-mode))
* recipients - a list of email addresses to send the message to
* subject - subject line of the email
* message - the email message
* template_vars _(optional)_ - custom variables passed to the template at runtime (see [Templating](#templating))

Both the subject and message can contain Jinja templates that are rendered at runtime.

### Running

To run the program using the following command:

```

.venv/bin/python3 blast.py -f messages/example-message.yaml

```

You can also run in test mode by using the `-T` flag. This will print the message information but not send anything.

```
.venv/bin/python3 blast.py -f messages/example-message.yaml -T
```

### Google SMTP Relay

It is possible to use Google as your SMTP relay if you have a Gmail address. Due to security concerns you must do some setup on your Google account first and generate an App Password to use as the login password for your account. Some instructions on how to do that are [here](https://saurabh-nakoti.medium.com/how-to-set-up-smtp-in-gmail-using-an-app-password-96adffa164b3)

## Templating

Both the email subject and message body can utilize [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/templates/) to insert dynamic content. Any of the built-in filters and functions of Jinja are available, along with a few custom ones.

* current_date - returns the current date/time as a Python datetime object, can be formatted with [strftime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
* parse_date - parse a string and return a datetime object

Custom variables can also be used within a message. These can be set using the `template_vars` key in the message template or passed in at runtime using the `-v` switch as follows:

```
.venv/bin/python3 blast.py -f messages/example-message.yaml -v var1=value1 -v var2=value2
```

This will result in two template variables being available as `{{ vars.var1 }}` and `{{ vars.var2 }}` in email templates. Do note that command line variables will replace variables of the same name if the exist within the message YAML file.

### Templates in Single Mode

When sending emails in single mode the template is rendered separately for each email. Because of this an additional global variable `email_address` is available and can be accessed within a template with `{{ email_address }}` or used with the `lookup_email` filter to map values for specific addresses. Imagine you want to insert the person's name at the top of your message. You could define a mapping as follows:

```
template_vars:
  names:
    email_address@domain.com: Person's Name
```

When running in __single mode__ you can lookup the name based on the email to automatically map the email key to the value.

```
Dear {{ vars.names | lookup_email }}
```

## License

[MIT](https://github.com/eau-claire-energy-cooperative/email-blaster/blob/main/LICENSE)
