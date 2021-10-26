# EMAIL CONFIGURATION AND SENDING TEST (PYTHON'S SMTPLIB, SSL, MIME LIBRARIES)

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "picprank.cs50@gmail.com"
sender_password = "Thisiscs50#"

receiver_email = input("Enter the receiver's email address: ")

message = MIMEMultipart("alternative")
message["Subject"] = "From PicPrank.CS50 with Laughters"
message["from"] = sender_email
message["to"] = receiver_email