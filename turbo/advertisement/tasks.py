from celery import shared_task
from .models import CarAdvertisement
from django.core.mail import send_mail
from django.conf import settings



def send_advertisement_mail(ad_id, subject_suffix, message_suffix):
    ad = CarAdvertisement.objects.get(id=ad_id)
    subject = f'Confirmation - {subject_suffix}'
    message = f'Hi {ad.your_name}. Your advertisement for {ad.name} {ad.model} was {message_suffix} successfully.'
    recipient_list = [ad.your_email]
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )
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