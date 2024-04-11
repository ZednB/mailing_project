import datetime

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from config import settings
from mail.forms import NewsletterForm
from django.core.mail import send_mail

from mail.models import NewsLetter, Client, Message, Log


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'mail/newsletter_list.html'


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')

    def send_news(request):
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
                return JsonResponse({'status': 'status', 'message': 'response'})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Sending settings not found'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})


class NewsLetterDetailView(DetailView):
    model = NewsLetter


class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    success_url = reverse_lazy('newsletter_list')


def send_new(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            newsletter = NewsLetter.objects.get(email=email)
            current_time = datetime.datetime.now().time()
            start_time = newsletter.start_time
            end_time = newsletter.end_time
            if start_time <= current_time <= end_time:
                clients = Client.objects.filter(newsletter=newsletter)
                for client in clients:
                    message = Message.objects.all()
                    log = Log.object.all()
                    status = log.status_try
                    response = log.response
                    theme = message.theme
                    body = message.body
                    send_mail(
                        subject=theme,
                        message=body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email]
                    )
                    return JsonResponse({'status': status, 'message': response})
            else:
                return JsonResponse({'status': 'error', 'message': 'Sending time not within the specified period'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sending settings not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})
