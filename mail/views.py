import datetime
import logging

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from config import settings
from mail.forms import NewsletterForm, MessageForm, ClientForm

from mail.models import NewsLetter, Client, Message, Log


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'mail/newsletter_list.html'


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')


class NewsLetterDetailView(DetailView):
    model = NewsLetter


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    success_url = reverse_lazy('newsletter_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mail/message_list.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mail/client_list.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')


class LogListView(ListView):
    model = Log
    template_name = 'mail/log_list.html'


def send_new(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            client = Client.objects.get(email=email)
            message = Message.objects.all()
            theme = message.theme
            body = message.body
            send_mail(
                subject=theme,
                message=body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email]
            )
            logging.info(f'Отправлено письмо на адрес {client.email} в {timezone.now()}')
            return JsonResponse({'status': 'status', 'message': 'response'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sending settings not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})





