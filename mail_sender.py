import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
#Flask and SQLAlchemy context (just for db access here)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model (same as in app.py)
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")

# Load HTML content
with open("index1.html", "r", encoding="utf-8") as f:
    html_content = f.read()

with app.app_context():
    # Get emails from database
    email_list = [subscriber.email for subscriber in Subscriber.query.all()]

    # Set up SMTP and send emails
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)

        for receiver_email in email_list:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Space Highlights You Don’t Want to Miss"
            msg["From"] = sender_email
            msg["To"] = receiver_email

            msg.attach(MIMEText(html_content, "html"))
            server.sendmail(sender_email, receiver_email, msg.as_string())

print("All emails sent!")
