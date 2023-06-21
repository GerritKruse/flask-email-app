from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

def send_email(user, password, recipient, subject, body):
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.strato.de', 587)
    server.starttls()
    server.login(user, password)
    text = msg.as_string()
    server.sendmail(user, recipient, text)
    server.quit()

@app.route('/')
def index():
    return '<h1>Flask is running!</h1>'

@app.route('/email', methods=['POST'])
def email_endpoint():
    data = request.get_json()
    recipient = data.get('recipient')
    body = data.get('body')
    subject = data.get('subject', 'No Subject') # default subject if not provided
    if recipient and body:
        try:
            send_email("info@wplacm.de", "iy9&jv%5M6&$9@D3", recipient, subject, body)
            return jsonify({'message': 'Email sent successfully'}), 200
        except Exception as e:
            return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'Recipient and body are required'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
