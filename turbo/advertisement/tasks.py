from celery import shared_task
from .models import CarAdvertisement, User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
import random
import logging


@shared_task
def test_task():
#     logger.info("Test task executed")
    return "Task completed"

def send_advertisement_mail(ad_id, subject_, message_):
    ad = CarAdvertisement.objects.get(id=ad_id)
    subject = f'Confirmation - {subject_}'
    ad_url = settings.SITE_URL + reverse('details', args=[ad.id])
    
    context = {
        'ad': ad,
        'subject': subject,
        'message_': message_,
        'ad_url': ad_url,
    }

    text_content = render_to_string('emails/add_message.txt', context)
    html_content = render_to_string('emails/add_message.html', context)
    
    recipient_list = [ad.your_email]

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True, 'Email sent successfully!'


# transaction.atomic()
@shared_task
def send_verify_code_mail_task(user_email, verification_code):
    send_mail(
            'Your Verification Code',
            f'Your verification code is {verification_code}',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    

@shared_task
def send_confirmation_mail_task(ad_id):
    return send_advertisement_mail(ad_id, 'Added', 'added')

@shared_task
def send_deleted_mail_task(ad_id):
    return send_advertisement_mail(ad_id, 'Deleted', 'deleted')

@shared_task
def send_update_notification_task(ad_id):
    return send_advertisement_mail(ad_id, 'Updated', 'updated')


# logger = logging.getLogger(__name__)

# @shared_task
# def send_verify_code_mail_task(email, verification_code):
#     logger.info(f"Task started for sending verification code to {email}")
#     print(f"Sending verification code to {email}")
#     # Your email sending code here
#     logger.info(f"Verification code sent to {email}")