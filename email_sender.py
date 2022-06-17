
import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def login():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(st.secrets["your_email"], st.secrets["your_password"])
    return server


def send_email(df,email):
    msg = MIMEMultipart()
    recipient = email
    from datetime import datetime
    todays_date = datetime.today().strftime('%d/%m/%Y')

    msg['Subject'] = "New Jobs for {}".format(todays_date)
    msg['From'] = st.secrets["your_email"]

    html = """\
    <html>
      <head></head>
      <body>
      Thank you for using using Grad Guide. Here are the best fitting jobs for you:
        {0}
      </body>
    </html>
    """.format(df.to_html(classes = ["table"], render_links = True, escape = False))

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = login()
    server.sendmail(msg['From'], recipient, msg.as_string())
    server.quit()

