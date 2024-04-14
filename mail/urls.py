from django.urls import path

from mail.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView, NewsLetterUpdateView, \
    NewsLetterDeleteView, MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, LogListView

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter_create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter'),
    path('newsletter_update/<int:pk>/', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>/', NewsLetterDeleteView.as_view(), name='newsletter_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('logs/', LogListView.as_view(), name='log_list')
]