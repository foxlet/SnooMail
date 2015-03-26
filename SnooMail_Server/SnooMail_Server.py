from flask import Flask, request
import requests

app = Flask(__name__)

id_from = "Example <support@example.com>"
remote_mailgun = "https://api.mailgun.net/v2/example.com/messages"

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
    id_no = 'test'

if __name__ == '__main__':
    app.run()
