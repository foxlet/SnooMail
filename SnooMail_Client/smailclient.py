'''
    smailclient.py - The Anope endpoint used to send messages to a relay.
    Copyright (C) 2014-2015 Foxlet <inquiries@comprepair.tk>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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
