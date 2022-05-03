import smtplib
from email.mime.text import MIMEText


def send_email(name, netid):
    assert isinstance(name, str), "Student name should be a string."
    assert isinstance(netid, str), "Student netid should be a string."

    gmail_user = 'tigermealx@gmail.com'
    gmail_password = 'Tigermealx1!'

    sent_from = gmail_user
    email = netid.lower().strip() + "@princeton.edu"
    to = [email]

    msg = MIMEText('You have successfully initiated your meal exchange with ' + name + '. Please complete both meals within 30 days!')
    msg['Subject'] = 'Meal Exchange Notification'
    msg['From'] = gmail_user
    msg['To'] = email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, msg.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong...",ex)

    return


def campus_dining_email(name, subject, msg):
    assert isinstance(name, str), "Student name should be a string."
    assert isinstance(subject, str), "Email subject should be a string."
    assert isinstance(subject, str), "Email message should be a string."

    gmail_user = 'tigermealx@gmail.com'
    gmail_password = 'Tigermealx1!'

    sent_from = gmail_user
    email = 'tigermealx@gmail.com'
    to = [email]

    msg = MIMEText(msg + "\n- " + name)
    msg['Subject'] = 'Meal Exchange Website Inquiry - ' + subject
    msg['From'] = gmail_user
    msg['To'] = email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, msg.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong...",ex)

    return

if __name__ == "__main__":
    send_email('Arin', 4)
    # campus_dining_email('Arin Mukherjee', 'complaint', 'I have a complaint.')
