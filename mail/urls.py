from django.urls import path

from mail.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter_create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter'),
]