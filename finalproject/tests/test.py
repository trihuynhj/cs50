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

# Create the plain-text and HTML version of your message
html = """\
<html>
  <body>
    <p>Hi, how are you?</p>
    <p>Here is some juicy pic for you! (haha)</p>
    <img alt="public-blowjob" src="http://uploadedporn.biz/uploads/posts/2018-07/1531416595_gc4zmvqkg9bnryw.jpg">
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
content = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(content)

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())