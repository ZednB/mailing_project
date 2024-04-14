import smtplib

from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mail.models import Log


def send_mails(mail):
    now = timezone.localtime(timezone.now())
    theme = mail.message.theme
    body = mail.message.body
    if mail.start_time <= now <= mail.end_time:
        for client in mail.client.all():
            try:
                send_mail(
                    theme,
                    body,
                    settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],
                    fail_silently=False
                )
                log = Log.objects.create(
                    date_time=mail.start_mail,
                    status_try='Успешно',
                    mailling_list=mail,
                    client=client.email
                )
                log.save()
            except smtplib.SMTPException as e:
                log = Log.objects.create(
                    date_time=mail.end_mail,
                    status_try='Ошибка,',
                    mailing_list=mail,
                    client=client.email
                )
            return log

