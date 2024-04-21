import logging
import random
import smtplib
from datetime import timedelta, datetime
from random import sample

from django.utils import timezone
from django.core.mail import send_mail

from blog.models import Blog
from config import settings
from mail.models import Log, NewsLetter, Client
from django.db.models import F


def mail_filter():
    date_time = timezone.now()
    mail_list = NewsLetter.objects.all()
    for mail in mail_list:
        end_mail = mail.end_mail
        # end_mail = datetime.combine(date_time.date(), end_mail)
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
        # start_mail = datetime.combine(date_time.date(), start_mail)
        # start_mail = start_mail.replace(tzinfo=date_time.tzinfo)
        end_mail = mail.end_mail
        # end_mail = datetime.combine(date_time.date(), end_mail)
        # end_mail = end_mail.replace(tzinfo=date_time.tzinfo)
        scheduled_time = mail.scheduled_time
        # scheduled_time = scheduled_time.replace(tzinfo=date_time.tzinfo)
        # scheduled_time = datetime.combine(date_time.date(), scheduled_time)

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


def list_main():
    mailing_count = NewsLetter.objects.all().count
    mailing_active_count = NewsLetter.objects.all().filter(status='created').count()
    client_count = Client.objects.all().count
    queryset_all = Blog.objects.all().filter(is_published=True)
    if queryset_all:
        queryset = random.choices(list(queryset_all), k=3)
    else:
        queryset = None

    context = {
        'mailing_count': mailing_count,
        'mailing_active_count': mailing_active_count,
        'client_count': client_count,
        'queryset': queryset,
    }
    return context
