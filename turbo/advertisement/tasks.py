from celery import shared_task
from .models import CarAdvertisement
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse


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

@shared_task
def send_confirmation_mail_task(ad_id):
    return send_advertisement_mail(ad_id, 'Added', 'added')

@shared_task
def send_deleted_mail_task(ad_id):
    return send_advertisement_mail(ad_id, 'Deleted', 'deleted')

@shared_task
def send_update_notification_task(ad_id):
    return send_advertisement_mail(ad_id, 'Updated', 'updated')