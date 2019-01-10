import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


def get_email_server():
    gmail_server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    gmail_server.login(os.environ['TEXT_CHELLA_EMAIL'], os.environ['TEXT_CHELLA_PASSWORD'])
    return gmail_server


def send_report(num_users, days_until_coachella):
    gmail_server = get_email_server()
    report = generate_report(num_users, days_until_coachella)
    gmail_server.sendmail(report['From'], 'sanjay.tamizharasu@gmail.com', report.as_string())
    gmail_server.sendmail(report['From'], 'johnroof8@gmail.com', report.as_string())
    gmail_server.close()


def generate_report(num_users, days_until_coachella):
    report = MIMEMultipart('mixed')
    report['From'] = 'textchella@gmail.com'
    report['Subject'] = 'Text Chella Daily Report For ' + datetime.datetime.today().strftime('%m-%d-%Y')
    report_body = MIMEText('Good Morning! \n' +
                           'Days until the Festival: ' + str(days_until_coachella) + '\n' 
                           'Daily Subscribers: ' + str(num_users) + '\n'
                           )
    report.attach(report_body)
    return report
