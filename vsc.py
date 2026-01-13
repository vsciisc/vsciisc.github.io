import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

URL = "https://vsciisc.github.io/meeting_notes.html"

GOOGLE_MEET_LINK = "https://meet.google.com/zfw-ahfa-qyp"

date = datetime.date.today() 
DATE = date.strftime("%dth %B %Y")
DATE_TIME = date.strftime("%dth %B %Y") + ", 6:30 - 8:30 PM."
#DATE_TIME = "13th January 2025-Tuesday(today), 6:30 - 8:30 PM."


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_lecture_link(soup: BeautifulSoup) -> str:
    """
    Extracts the lecture PDF link dynamically.
    Assumes lecture links end with .pdf
    """
    pdf_links = soup.find_all("a", href=True)
    for link in pdf_links:
        href = link["href"]
        if href.lower().endswith(".pdf"):
            # Handle relative URLs
            if href.startswith("http"):
                return href
            else:
                return f"https://vsciisc.github.io/{href.lstrip('/')}"
    raise ValueError("Lecture PDF link not found")


def extract_meeting_minutes(soup: BeautifulSoup) -> list:
   
    heading = None
    for tag in soup.find_all(["details"]):

        #print(tag)
        
        text = str(tag)

        items = re.findall(r"<li>(.*?)</li>", text, )
        break
      
    return items


def generate_email_body(lecture_link: str, minutes: list) -> str:
    body = f"""Namaskaram,

Welcome to VSC IISc weekly class.

Date and Time:- {DATE_TIME}.

Venue: Warden Room, 1st floor, A Block Hostel, above A Mess, IISc.

Google Maps Link: https://maps.app.goo.gl/HMja5vR2ce4EQ85GA

We encourage the IISc community to attend the VSC classes in person.If you are unable to make it today, you may join the class online using this Google Meet link: 
{GOOGLE_MEET_LINK}

Today's lecture: {lecture_link}

Meeting minutes of last class:
"""
    for i, point in enumerate(minutes, start=1):
        body += f"{i}. {point}\n"

    body += """
Regards
VSC Team
Contact:- Mohit (9472464127)
"""
    return body

def send_email(SENDER_EMAIL, RECIPIENTS, SUBJECT, EMAIL_BODY):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(EMAIL_BODY, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print("Email sent successfully!")


if __name__ == "__main__":
    soup = fetch_page(URL)
    lecture_link = extract_lecture_link(soup)
    meeting_minutes = extract_meeting_minutes(soup)
    
    
    EMAIL_BODY = generate_email_body(lecture_link, meeting_minutes)
    


    SENDER_EMAIL = "vsciisc07@gmail.com"
    APP_PASSWORD = "qqudijtzjirbfxgp"


    RECIPIENTS = [
        "vsc-iisc@googlegroups.com"
    ]

    SUBJECT = f'''{{VSC-IISc}} Gentle reminder for the VSC Session on {DATE}'''
    print(SUBJECT)
    print(EMAIL_BODY)
    send_email(SENDER_EMAIL, RECIPIENTS, SUBJECT, EMAIL_BODY)