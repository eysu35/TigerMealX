import smtplib


def send_email(name):
    gmail_user = 'tigermealx@gmail.com'
    gmail_password = 'Tigermealx1!'
    # gmail_password = 'input("Type your password and press enter: ")'

    sent_from = gmail_user
    to = ['arinm@princeton.edu']
    # to = ['tigermealx@gmail.com']
    subject = 'Meal Exchange Notification'
    body = 'Scan this barcode when completing your meal exchange with ' + name + '.'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong...",ex)

    return

if __name__ == "__main__":
    send_email('auguste')