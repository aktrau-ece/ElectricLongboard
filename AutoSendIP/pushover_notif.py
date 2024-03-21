#!/usr/bin/env python3

from pprint import pformat
import subprocess
from time import sleep

from pushover import Client

user_key = 'usiy1jsb5zdx1pffknnd5nqre5sifd'
api_token = 'abmpxzwfgzyd52vhipw2vjycn6a5og'

# Wait for RPi to connect to the internet
sleep(10)

ip_addr = subprocess.check_output(['hostname', '-I']).decode('utf-8')
print(f'Hostname: {ip_addr}')

client = Client(user_key, api_token=api_token)
client.send_message(f'Here is my IP address: {ip_addr}', title='RPi Login')