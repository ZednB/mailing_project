import smtplib
from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mail.models import Log, NewsLetter
from django.db.models import F


def send_mails():
    now = timezone.localtime(timezone.now())
    mail_list = NewsLetter.objects.filter(start_mail=now)
    # if mail_list.start_mail <= now <= mail_list.end_mail:
    for mail in mail_list:
        theme = mail_list.message.theme
        body = mail_list.message.body
        try:
            send_mail(
                theme,
                body,
                settings.EMAIL_HOST_USER,
                recipient_list=[mail.client.email],
                fail_silently=False
            )
            if mail.periodicity == 'daily':
                mail.sent_time = F('start_mail') + timedelta(days=1)
                mail.mailing_status = 'launched'
            elif mail.periodicity == 'weekly':
                mail.sent_time = F('start_mail') + timedelta(days=7)
                mail.mailing_status = 'launched'
            elif mail.periodicity == 'monthly':
                mail.sent_time = F('start_mail') + timedelta(days=30)
                mail.mailing_status = 'launched'
            mail.save()
            log = Log.objects.create(
                date_time=mail.start_mail,
                status_try='Успешно',
                mailling_list=mail,
                client=mail.client.email
            )
            log.save()
        except smtplib.SMTPException as e:
            log = Log.objects.create(
                date_time=mail.end_mail,
                status_try='Ошибка,',
                mailing_list=mail,
                client=mail.client.email
            )
        return log

