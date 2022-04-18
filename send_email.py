import smtplib
from email.mime.text import MIMEText


def send_email(name, netid):
    gmail_user = 'tigermealx@gmail.com'
    gmail_password = 'Tigermealx1!'

    sent_from = gmail_user
    to = ['arinm@princeton.edu']
    email = netid.lower().strip() + "@princeton.edu"
    to = [email]

    # to = ['tigermealx@gmail.com']
    # subject = 'Meal Exchange Notification'
    # body = 'You have successfully initiated your meal exchange with '\
    #        + name + '. Please complete both meals within 30 days!'
    #
    # email_text = """\
    # From: %s
    # To: %s
    # Subject: %s
    #
    # %s
    # """ % (sent_from, ", ".join(to), subject, body)

    msg = MIMEText('You have successfully initiated your meal exchange with ' + name + '. Please complete both meals within 30 days!')
    msg['Subject'] = 'Meal Exchange Notification'
    msg['From'] = gmail_user
    msg['To'] = email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        # smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.sendmail(sent_from, to, msg.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong...",ex)

    return


if __name__ == "__main__":
    send_email('auguste')