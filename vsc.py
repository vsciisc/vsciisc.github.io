import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://vsciisc.github.io/meeting_notes.html"

GOOGLE_MEET_LINK = "https://meet.google.com/zfw-ahfa-qyp"


# ---------- Date Formatting ----------

def ordinal(n):
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{ {1:'st',2:'nd',3:'rd'}.get(n%10, 'th') }"


today = datetime.date.today()

DATE = f"{ordinal(today.day)} {today.strftime('%B %Y')}"
DATE_TIME = f"{ordinal(today.day)} {today.strftime('%B %Y')}, 6:30 - 8:30 PM."


# ---------- Fetch Page ----------

def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# ---------- Extract Lecture PDF ----------

def extract_lecture_link(soup: BeautifulSoup) -> str:

    for tag in soup.find_all("a", href=True):

        if tag["href"].endswith(".pdf"):
            return tag["href"]

    return "Lecture link not found"


# ---------- Extract Meeting Minutes ----------

def extract_meeting_minutes(soup: BeautifulSoup) -> list:

    minutes = []

    details = soup.find("details")

    if details:
        for li in details.find_all("li"):
            minutes.append(li.get_text(strip=True))

    return minutes


# ---------- Generate Email Body ----------

def generate_email_body(lecture_link: str, minutes: list) -> str:

    body = f"""Namaskaram,

Welcome to VSC IISc weekly class.

Date and Time: {DATE_TIME}

Venue: Warden Room, 1st floor, A Block Hostel, above A Mess, IISc.

Google Maps Link:
https://maps.app.goo.gl/HMja5vR2ce4EQ85GA

We encourage the IISc community to attend the VSC classes in person.
If you are unable to make it today, you may join the class online using this Google Meet link:

{GOOGLE_MEET_LINK}

Today's lecture:
{lecture_link}

Meeting minutes of last class:
"""

    for i, point in enumerate(minutes, start=1):
        body += f"{i}. {point}\n"

    body += """

Regards
VSC Team

Contact: Mohit (9472464127)
"""

    return body


# ---------- Send Email ----------

def send_email(sender_email, app_password, recipients, subject, email_body):

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(email_body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("Email sent successfully!")


# ---------- Main ----------

if __name__ == "__main__":

    soup = fetch_page(URL)

    lecture_link = extract_lecture_link(soup)

    meeting_minutes = extract_meeting_minutes(soup)

    EMAIL_BODY = generate_email_body(lecture_link, meeting_minutes)

    SUBJECT = f"{{VSC-IISc}} Gentle reminder for the VSC Session on {DATE}"

    SENDER_EMAIL = os.getenv("EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    RECIPIENTS = [
        "vsc-iisc@googlegroups.com"#"psangeerthgenius@gmail.com"
    ]
#
    print(SUBJECT)
    print(EMAIL_BODY)

    send_email(SENDER_EMAIL, APP_PASSWORD, RECIPIENTS, SUBJECT, EMAIL_BODY)