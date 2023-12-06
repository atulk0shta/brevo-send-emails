from __future__ import print_function
import logging
from logging.config import fileConfig
import os

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()
fileConfig(os.getenv('LOGGING_CONFIG_FILE_PATH'))


logger = logging.getLogger()

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key[
    'api-key'] = os.getenv('BREVO_KEY')


def send_email(to_addresses, subject, html_content, bcc=None, reply_to=None):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": os.getenv('SENDER_NAME'), "email": os.getenv('SENDER_EMAIL')}
    headers = {'Content-Type': 'application/json'}

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to_addresses,
                                                   bcc=bcc,
                                                   headers=headers,
                                                   html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(api_response)
    except ApiException as e:
        logger.error("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


toAddresses = [{'email': 'toemail@example.com', 'name': 'W. Bose'}]
bcc = [{'email': 'email@example.com', 'name': 'Name'}]
subject = "Test email subject"
htmlContent = "<html><body><h1>This is my first transactional email </h1></body></html>"
send_email(toAddresses, subject, htmlContent, bcc=bcc)
