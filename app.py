from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load SMTP credentials from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "hithesh2201@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email_route():
    try:
        sender_email = request.form['senderEmail']
        receiver_emails = request.form['receiverEmails'].split(',')
        subject = request.form['subject']
        body = request.form['body']
        
        pdf_attachment = request.files.get('pdfAttachment')
        pdf_filename = None
        if pdf_attachment and pdf_attachment.filename != "":
            pdf_filename = os.path.join(UPLOAD_FOLDER, pdf_attachment.filename)
            pdf_attachment.save(pdf_filename)

        send_email(sender_email, receiver_emails, subject, body, pdf_filename)

        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def send_email(sender_email, receiver_emails, subject, body, pdf_filename=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if pdf_filename:
        with open(pdf_filename, 'rb') as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_filename))
            msg.attach(pdf_attachment)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_emails, msg.as_string())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
