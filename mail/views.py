from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from mail.forms import NewsletterForm, MessageForm, ClientForm, ModeratorNewsletterForm

from mail.models import NewsLetter, Client, Message, Log

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class NewsLetterListView(LoginRequiredMixin, ListView):
    model = NewsLetter
    template_name = 'mail/newsletter_list.html'

    def get_queryset(self):
        if self.request.user.has_perm('mail.view_all_mails'):
            newsletter_list = super().get_queryset()
        else:
            newsletter_list = super().get_queryset().filter(owner=self.request.user)
        return newsletter_list


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    model = NewsLetter


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')

    def get_form_class(self):
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return NewsletterForm
        elif self.request.user.has_perm('mail.deactivate_mails'):
            return ModeratorNewsletterForm
        else:
            raise Http404('У вас недостаточно прав для редактирования')


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetter
    success_url = reverse_lazy('newsletter_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mail/message_list.html'

    # def get_queryset(self):
    #     if self.request.user.has_perm('mailing.view_all_mailings'):
    #         mailing_list = super().get_queryset()
    #     else:
    #         mailing_list = super().get_queryset().filter(owner_id=self.request.user)
    #     return mailing_list


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message_list')

    def get_form_class(self):
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return MessageForm
        else:
            raise Http404('У вас недостаточно прав для редактирования')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message_list')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mail/client_list.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    template_name = 'mail/log_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

# def send_new(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         try:
#             client = Client.objects.get(email=email)
#             message = Message.objects.all()
#             theme = message.theme
#             body = message.body
#             send_mail(
#                 subject=theme,
#                 message=body,
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[client.email]
#             )
#             logging.info(f'Отправлено письмо на адрес {client.email} в {timezone.now()}')
#             return JsonResponse({'status': 'status', 'message': 'response'})
#         except ObjectDoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Sending settings not found'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'})
