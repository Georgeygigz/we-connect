"""Module for handling sending of emails."""

from flask import render_template
from flask_mail import Message

from main import celery_app
from manage import app, mail


class Email:

    """Class for sending emails."""
    # DEFAULT_RECIPIENT =

    # @staticmethod
    # @celery_app.task(name='send_smtp_email')
    # def send_mail(title, recipients, body, attachment_data={}):
    #     """Sends an email using smtp.gmail.com mail server
    #     Args:
    #         title (str): Title of the email to be sent
    #         recipients (list): A list containing the emails of recipients
    #         body (string): The body of the mail to be sent
    #         error (bool): The type of mail to send (success or error)
    #         attachment_data (dict): A dict with a StringIO object and a filename
    #     Raises:
    #         ValidationError: exception raised if email sending fails
    #     """
    #     with app.app_context():
    #         message = Message(title, recipients=recipients, body=body)
    #         message.html = render_template('verify.html', **{
    #         'link': AppConfig.VERIFY_URL,
    #         'first_name': 'first_name'
    #         })
    #         mail.send(message)

    @staticmethod
    @celery_app.task(name='send_smtp_email')
    def send_mail_with_template(title, recipient, template_id, template_data):
        """Class method for sending template emails using SendGrid API

       Args:
           recipient (str): the receiving email address.
           template_id (str): the SendGrid transactional template id
           template_data (dict): data to populate the template.

       Returns:
           dict: returns a dictionary containing status, headers and body  on success.
           Bool: returns a boolean False on failure.

       """
        with app.app_context():
            message = Message(title, recipients=recipient, body='Body')
            message.html = render_template(template_id, **template_data)
            mail.send(message)
