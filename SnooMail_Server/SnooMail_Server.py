from flask import Flask, request
import requests

app = Flask(__name__)

id_from = "Example <support@example.com>"
remote_mailgun = "https://api.mailgun.net/v2/example.com/messages"
remote_brimir = "https://brimir.example.com/{}"

def get_token(user, password):
    auth = requests.post(remote_brimir.format('api/v1/sessions'), data={'email': user,'password': password}).json()
    return auth['authorization_token']

@app.route('/send', methods=['POST'])
def send_msg():
    id_to = request.form['to']
    id_contents = request.form['contents']
    id_privkey = request.form['key']
    id_subject = request.form['subject']

    data = requests.post(remote_mailgun,
                auth=("api", id_privkey),
                data={"from": id_from,
                    "to": id_to,
                    "subject": id_subject,
                    "text": id_contents})

    return data.text

@app.route('/receive', methods=['POST'])
def recv_msg():
    msg_route = {}
    msg_route['recipient'] = request.form['recipient']
    msg_route['sender'] = request.form['sender']
    msg_route['body'] = request.form['body-plain']
    msg_route['from'] = request.form['From']
    msg_route['to'] = request.form['To']
    msg_route['subject'] = request.form['Subject']

    # May be needed in the future? Currently not used
    # token = get_token('', '')
    # request_url = 'tickets.json?auth_token={}'.format(token)
    request_url = 'tickets.json'

    email = 'To: {}\n'\
            'Subject: {}\n'\
            'From: {}\n'\
            '\n{}'.format(msg_route['to'], msg_route['subject'], msg_route['from'], msg_route['body'])

    print(email)

    payload = requests.post(remote_brimir.format(request_url),
                data={'message': email})

    return payload.text

if __name__ == '__main__':
    app.run()
