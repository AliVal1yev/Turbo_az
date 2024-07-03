from django.test import TestCase
from .views import mail_message, send_mail
from django.conf import settings


# Create your tests here.


class MailMessageTests(TestCase):
    def test_mail_message_sending(self, email):
        subject = 'Confirmation'
        message = 'Your advertisement was added successfully'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
            )
        
        self.assertTrue(mail_message(email='alivaliyev150@gmail.com'), True)