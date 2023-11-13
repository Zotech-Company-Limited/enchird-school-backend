import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import smtplib
from io import BytesIO
from django.core.mail import send_mail
from django.template.loader import render_to_string

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "jvperezmbi@gmail.com"  # Enter your address

password = 'qamgdgifrpkuikdn'

def send_plaintext(user, message):
    try:
        context = ssl.create_default_context()

        # Create a connection to the SMTP server using SSL
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            # Log in to your SMTP server using your credentials
            server.login(sender_email, password)

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.email
            msg['Subject'] = "TEST MESSAGE"
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(sender_email, user.email, msg.as_string())

            # Close the connection
            server.quit()

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def send_verification_email(user, reset_token):
    try:
        context = ssl.create_default_context()

        # Create a connection to the SMTP server using SSL
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            # Log in to your SMTP server using your credentials
            server.login(sender_email, password)

            # Create the verification link using the token
            verification_link = f"http://localhost:8000/verify-email/{reset_token}/"

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.email
            msg['Subject'] = "Enchird Email Verification"

            # Include the verification link in the email body
            email_body = f"Hello {user.first_name}, \n\nClick the following link to verify your email:\n{verification_link}"

            msg.attach(MIMEText(email_body, 'plain'))

            server.sendmail(sender_email, user.email, msg.as_string())

            # Close the connection
            server.quit()

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


def send_reset_password_email(user, reset_token, uid):
    try:
        context = ssl.create_default_context()

        # Create a connection to the SMTP server using SSL
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            # Log in to your SMTP server using your credentials
            server.login(sender_email, password)

            # Create the verification link using the token
            verification_link = f"https://frontend.zotechinsights.com/createnewpassword?uid={uid}&token={reset_token}/"

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.email
            msg['Subject'] = "Reset Password"

            # Include the verification link in the email body
            email_body = f"Hello {user.first_name}, \n\nClick the following link to reset your password:\n{verification_link}"

            msg.attach(MIMEText(email_body, 'plain'))

            server.sendmail(sender_email, user.email, msg.as_string())

            # Close the connection
            server.quit()

        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False




def send_adminhtmltext(user, content):

    message = MIMEMultipart("alternative")
    message["Subject"] = content['subject']
    message["From"] = sender_email
    message["To"] = user

    print("\nMESSAGE IS:\n")
    print(message)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(content['text'], "plain")
    part2 = MIMEText(content['html'], "html")

    print("\nMESSAGE PARTS\n")
    # print(part1)
    # print(part2)

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    print("\nMESSAGE ATTACHMENT\n")
    # print(message)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, message['To'], message.as_string()
        )

        print("\nIS DONE\n")

    print("\nDONE CODE EXECUTION\n")

    return None


def send_htmltext(user, content):

    message = MIMEMultipart("alternative")
    message["Subject"] = content['subject']
    message["From"] = sender_email
    message["To"] = user.email

    print("\nMESSAGE IS:\n")
    print(message)

    # Turn these into plain/html MIMEText objects
    # part1 = MIMEText(content['text'], "plain")
    part2 = MIMEText(content['html'], "html")

    print("\nMESSAGE PARTS\n")
    # print(part1)
    # print(part2)

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    # message.attach(part1)
    message.attach(part2)

    print("\nMESSAGE ATTACHMENT\n")
    # print(message)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, message['To'], message.as_string()
        )

        print("\nIS DONE\n")

    print("\nDONE CODE EXECUTION\n")

    return None


