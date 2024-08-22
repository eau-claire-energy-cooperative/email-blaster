# Email Blaster
[![License](https://img.shields.io/github/license/eau-claire-energy-cooperative/email-blaster)](https://github.com/eau-claire-energy-cooperative/email-blaster/blob/main/LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg)](https://github.com/RichardLitt/standard-readme)

Sometimes you just have to blast out some emails. This is a rather simple Python script to pull in some email template files and send them through your configured SMTP service. Works with a public service like Gmail or your own SMTP. This is useful if you have emails that need to go out on a timer or perhaps have some dynamic content you want to set per message as they're sent.

Message files are configured using YAML and can contain [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/templates/) to insert dynamic content.

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
pip3 install -r install/requirements.txt

# deactivate virtual environment when done
deactivate

```

## Usage

## License

[MIT](https://github.com/eau-claire-energy-cooperative/email-blaster/blob/main/LICENSE)
