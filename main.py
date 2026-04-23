from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import uuid
import psycopg
from datetime import datetime
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking

load_dotenv()

sender = os.getenv("SENDER")
api = os.getenv("SEND_GRID_API")
sg = SendGridAPIClient(api)

EMAIL_TYPES = {
    1: ("Phising_Email_Sim/email_templates/password_mail.html", "password_reset"),
    2: ("Phising_Email_Sim/email_templates/order_confirmation.html", "order_confirmation"),
    3: ("Phising_Email_Sim/email_templates/impersonation.html", "impersonation"),
    4: ("Phising_Email_Sim/email_templates/quishing.html", "quishing"),
}

def get_db():
    return psycopg.connect(os.getenv("DATABASE_URL"))

def create_tracking_link(email, email_type, destination):
    token = str(uuid.uuid4())

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO link_clicks (token, email, email_type, sent_at) VALUES (%s, %s, %s, %s)",
        (token, email, email_type, datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()

    return f"http://localhost:5000/track?token={token}&redirect={destination}"

def choosing():
    receiver = input("Type in receiver mail: ")

    while True:
        print("1 - Password Reset\n2 - Order Confirmation\n3 - Impersonation\n4 - Quishing")
        choice = int(input("Choose phishing email type (1-4): "))
        if choice in EMAIL_TYPES:
            template_path, email_type = EMAIL_TYPES[choice]
            return template_path, email_type, receiver
        else:
            print("Invalid selection. Please choose between 1-4")

def sending(template, email_type, receiver):
    tracking_link = create_tracking_link(
        email=receiver,
        email_type=email_type,
        destination="https://www.youtube.com/watch?v=__rmRp6S-l8"
    )

    with open(template, "r", encoding="utf-8") as file:
        htmlcontent = file.read()

    htmlcontent = htmlcontent.replace("{{TRACKING_LINK}}", tracking_link)

    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject="Problem Occurred",
        html_content=htmlcontent
    )

    # Disable SendGrid's own click tracking
    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    message.tracking_settings = tracking_settings

    print("ABOUT TO SEND")
    response = sg.send(message)
    print("SENT")
    print(response.status_code)

template, email_type, receiver = choosing()
sending(template, email_type, receiver)