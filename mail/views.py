from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from mail.forms import NewsletterForm

from mail.models import NewsLetter


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'mail/newsletter_list.html'


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter_list')


class NewsLetterDetailView(DetailView):
    model = NewsLetter
