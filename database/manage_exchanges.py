import schedule
from datetime import datetime, date
import smtplib
from exchanges import Exchanges
from students import Students

def send_email(email_address, subject, msg):
    gmail_user = 'tigermealx@gmail.com'
    gmail_password = 'Tigermealx1!'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_password)
    subject = subject
    to = email_address
    msg = msg
    body = "Subject: {}\n\n{}".format(subject, msg)
    smtpserver.sendmail(gmail_user, to, body)
    smtpserver.close()
    print("success sending email")


def notify():
    expired_exchanges_ids, one_week_exchanges_ids, \
    three_day_exchanges_ids = Exchanges.update_exchange_status()

    for exchange_id in expired_exchanges_ids:
        netid1, netid2 = Exchanges.get_netid_from_mealx_id(exchange_id)
        email1 = netid1 + "@princeton.edu"
        email2 = netid2 + "@princeton.edu"

        subject = "Meal Exchange Expiration Notice"

        message1 = "Dear " + \
            str(Students.get_first_name_from_netid(netid1)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid2)) + " has " \
            "expired on " + str(date.today()) + ". Please contact " \
            "tigermealx@gmail.com with any questions. \n"

        message2 = "Dear " + \
            str(Students.get_first_name_from_netid(netid2)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid1)) + " has " \
            "expired on " + str(date.today()) + ". Please contact " \
            "tigermealx@gmail.com with any questions. \n"

        send_email(email1, subject, message1)
        send_email(email2, subject, message2)

        # notify locations later when we have their emails


    for exchange_id in one_week_exchanges_ids:
        netid1, netid2 = Exchanges.get_netid_from_mealx_id(exchange_id)
        email1 = netid1 + "@princeton.edu"
        email2 = netid2 + "@princeton.edu"

        subject = "Meal Exchange Expiring In One Week!"

        message1 = "Dear " + \
            str(Students.get_first_name_from_netid(netid1)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid2)) + \
            " will expire in 7 days. Please exchange your second meal "\
            "within the week or contact tigermealx@gmail.com with any" \
            " questions. \n"

        message2 = "Dear " + \
            str(Students.get_first_name_from_netid(netid2)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid1)) + \
            " will expire in 7 days. Please exchange your second meal "\
            "within the week or contact tigermealx@gmail.com with any" \
            " questions. \n"

        send_email(email1, subject, message1)
        send_email(email2, subject, message2)

    for exchange_id in three_day_exchanges_ids:
        netid1, netid2 = Exchanges.get_netid_from_mealx_id(exchange_id)
        email1 = netid1 + "@princeton.edu"
        email2 = netid2 + "@princeton.edu"

        subject = "Meal Exchange Expiring In Three Days!"

        message1 = "Dear " + \
            str(Students.get_first_name_from_netid(netid1)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid2)) + \
            " will expire in 3 days. Please exchange your second meal "\
            "within that time or contact tigermealx@gmail.com with " \
            "any questions. \n"

        message2 = "Dear " + \
            str(Students.get_first_name_from_netid(netid2)) + \
            ",\n This is a notice that your meal exchange with " \
            + str(Students.get_full_name_from_netid(netid1)) + \
            " will expire in 7 days. Please exchange your second meal "\
            "within that time or contact tigermealx@gmail.com with " \
            "any questions. \n"

        send_email(email1, subject, message1)
        send_email(email2, subject, message2)

# manage exchanges every day at 9:00 am Eastern time
schedule.every().day.at("09:00").do(notify)