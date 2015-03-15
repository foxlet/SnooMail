__author__ = 'foxlet'

import fileinput
import email
import requests
import json
import sys

data = []
remote = "http://127.0.0.1:80/send"
privkey = "GET_YOUR_OWN_KEY"

for line in fileinput.input():
    data.append(line)

message = email.message_from_string("".join(data))

msg_to = message["To"]
msg_subject = message["Subject"]
if msg_subject is None:
    msg_subject = "FurCode Services Message"
msg_contents = message.get_payload()

headers = {'Authorization': 'Client-ID ' + privkey}

client = requests.post(remote, data={'key': privkey, 'to': msg_to, 'subject': msg_subject, 'contents': msg_contents}, headers = headers, verify=False)

try:
    val = json.loads(client.text)
except ValueError:
    print(client.text)
    sys.exit(1)

try:
    print(val['id'])
except KeyError:
    print(val['message'])