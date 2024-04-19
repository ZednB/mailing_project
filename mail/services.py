import logging
import smtplib
from datetime import timedelta, datetime

from django.utils import timezone
from django.core.mail import send_mail

from config import settings
from mail.models import Log, NewsLetter, Client
from django.db.models import F


def mail_filter():
    date_time = datetime.now()
    mail_list = NewsLetter.objects.all()
    for mail in mail_list:
        end_mail = mail.end_mail
        end_mail = datetime.combine(date_time.date(), end_mail)
        if end_mail <= date_time:
            mail.status = 'ended'
            mail.save()
        else:
            ...
    mail_filtered = NewsLetter.objects.filter(status='created')
    print(mail_filtered)
    send_mails(mail_filtered)


def send_mails(mailing):
    logging.info('send_mails')
    date_time = timezone.now()
    # date_time = date_time.replace(tzinfo=timezone.utc)
    for mail in mailing:
        start_mail = mail.start_mail
        start_mail = datetime.combine(date_time.date(), start_mail)
        start_mail = start_mail.replace(tzinfo=date_time.tzinfo)
        end_mail = mail.end_mail
        end_mail = datetime.combine(date_time.date(), end_mail)
        end_mail = end_mail.replace(tzinfo=date_time.tzinfo)
        scheduled_time = mail.scheduled_time
        scheduled_time = scheduled_time.replace(tzinfo=date_time.tzinfo)
        scheduled_time = datetime.combine(date_time.date(), scheduled_time)

        if start_mail <= date_time <= end_mail and date_time >= scheduled_time:
            mail.status = 'sent'
            theme = mail.message.theme
            body = mail.message.body
            clients = mail.client.all()
            for client in clients:
                client_email = client.email
            # client_email = [client.email for client in clients]

                try:
                    status = send_mail(
                        subject=theme,
                        message=body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client_email],
                        fail_silently=False
                    )
                    Log.objects.create(
                        status_try=status,
                        mailing_list=mail
                    )
                except smtplib.SMTPException as e:
                    Log.objects.create(
                        status_try=False,
                        mailing_list=mail,
                        response=e
                    )
                if mail.frequency == 'daily':
                    mail.scheduled_time = date_time + timedelta(days=1)
                    mail.status = 'created'
                elif mail.frequency == 'weekly':
                    mail.scheduled_time = date_time + timedelta(days=7)
                    mail.status = 'created'
                elif mail.frequency == 'monthly':
                    mail.scheduled_time = date_time + timedelta(days=30)
                    mail.status = 'created'
                else:
                    mail.status = 'ended'
                mail.save()

# def send_mails():
#     now = timezone.localtime(timezone.now())
#     mail_list = NewsLetter.objects.filter(start_mail=now)
#     print(mail_list)
#     # if mail_list.start_mail <= now <= mail_list.end_mail:
#     for mail in mail_list:
#         theme = mail.message.theme
#         body = mail.message.body
#         print(theme, body)
#         client_list = Client.objects.all()
#         for client in client_list:
#             client = client.email
#             try:
#                 send_mail(
#                     subject=theme,
#                     message=body,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[client.email],
#                     fail_silently=False
#                 )
#                 if mail.periodicity == 'daily':
#                     mail.sent_time = F('start_mail') + timedelta(days=1)
#                     mail.mailing_status = 'sent'
#                 elif mail.periodicity == 'weekly':
#                     mail.sent_time = F('start_mail') + timedelta(days=7)
#                     mail.mailing_status = 'sent'
#                 elif mail.periodicity == 'monthly':
#                     mail.sent_time = F('start_mail') + timedelta(days=30)
#                     mail.mailing_status = 'sent'
#                 mail.save()
#                 print(mail)
#                 log = Log.objects.create(
#                     date_time=mail.start_mail,
#                     status_try='Успешно',
#                     mailling_list=mail,
#                     client=client.email
#                 )
#                 log.save()
#                 print(log)
#             except smtplib.SMTPException as e:
#                 log = Log.objects.create(
#                     date_time=mail.end_mail,
#                     status_try='Ошибка,',
#                     mailing_list=mail,
#                     client=client.email
#                 )
#             return log
