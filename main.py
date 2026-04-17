from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("SENDER")
api = os.getenv("SEND_GRID_API")
sg = SendGridAPIClient(api)

def choosing():
    templates = {

        1: "Phising_Email_Sim\email_templates\password_mail.html"

    }

    receiver = input("Type in receiver mail: ")

    while True:
        choice = int(input("Choose phishing email type (1-4): "))
        if choice in templates:
            return templates[choice], receiver
        else:
            print("Invalid selection. Please choose between 1-4")

def sending(template, receiver):
    with open(f"{template}", "r", encoding="utf-8") as file:
        htmlcontent = file.read()

    message = Mail(
    from_email=sender,
    to_emails=receiver,
    subject="Problem Occurred",
    html_content=htmlcontent
    )

    

    print("ABOUT TO SEND")
    response = sg.send(message)
    print("SENT")

    print(response.status_code)
    print(response.body)
    print(response.headers)

template, receiver = choosing()
sending(template, receiver)
