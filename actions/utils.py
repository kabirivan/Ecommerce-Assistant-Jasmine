import logging
import os
import json
import smtplib
import traceback
# from pyairtable import Api, Base, Table
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)
email_username = os.getenv('EMAIL_USERNAME')
email_password = os.getenv('EMAIL_PASSWORD')
base_id = os.getenv('BASE_ID')
table_name = os.getenv('TABLE_NAME')
api_key_airtable = os.getenv('API_KEY_AIRTABLE')

def send_email(subject: str, recipient_email: str, content):
    try:
        username = email_username
        password = email_password

        message_data = MIMEMultipart()
        message_data["From"] = username
        message_data["To"] = recipient_email
        message_data["Subject"] = subject

        message_data.attach(MIMEText(content, "html"))
        msgBody = message_data.as_string()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.sendmail(username, recipient_email, msgBody)
        return True

    except Exception as error:
        logger.error(f"Error: {error}")
        logger.info(traceback.print_exc())
        return False


def get_html_data(filepath: str):
    with open(filepath, "r") as html_data:
        return html_data.read()



new_record = {
    "name": "Gabriela",
    "email": "gabriela.sanchez@epn.edu.ec",
    "feedback_value": "3",
    "feedback_message": "Me gusta el diseno",
    "created_at": "2022-01-10"
}
#airtable_upload(table_name, new_record, False, api_key_airtable, base_id, None)
# table = Table('api_key_airtable', 'base_id', 'table_name')
# table.create(new_record)