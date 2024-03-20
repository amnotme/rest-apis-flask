import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MAILGUN_API_KEY")
domain_name = os.getenv("MAILGUN_DOMAIN")
email = os.getenv("MAIL_GUN_EMAIL")

def send_simple_message(to, subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", api_key),
        data={
            "from": f"Leo Hernandez <mailgun@{domain_name}>",
            "to": [to],
            "subject": subject,
            "text": body,
        },
    )


def send_user_registration_email(username):
    return send_simple_message(
        email, "Successfully signed up", f"Hi, Someone signed up! {username} successfully signed up."
    )
