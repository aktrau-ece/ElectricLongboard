from pprint import pformat
import subprocess

from pushover import Client

user_key = 'usiy1jsb5zdx1pffknnd5nqre5sifd'
api_token = 'abmpxzwfgzyd52vhipw2vjycn6a5og'

sp_output = subprocess.check_output(['hostname', '-I'])
hostname = sp_output.decode("utf-8")
print(f'Hostname: {hostname}')

client = Client(user_key, api_token=api_token)
client.send_message("Heres my IP address", title="RPi Login")