import os
import requests
from dotenv import load_dotenv
import jinja2

load_dotenv()

api_key = os.getenv("MAILGUN_API_KEY")
domain_name = os.getenv("MAILGUN_DOMAIN")
email = os.getenv("MAIL_GUN_EMAIL")

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader, autoescape=True)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{domain_name}/messages",
        auth=("api", api_key),
        data={
            "from": f"Leo Hernandez <mailgun@{domain_name}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html
        },
    timeout=60)


def send_user_registration_email(username):
    return send_simple_message(
        to=email,
        subject="Successfully signed up",
        body=f"Hi, Someone signed up! {username} successfully signed up.",
        html=render_template("email/action.html", username=username)
    )
