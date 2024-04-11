from django.urls import path

from mail.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView, NewsLetterUpdateView, \
    NewsLetterDeleteView

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='newsletter_list'),
    path('newsletter_create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/', NewsLetterDetailView.as_view(), name='newsletter'),
    path('newsletter_update/<int:pk>/', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>/', NewsLetterDeleteView.as_view(), name='newsletter_delete'),
]