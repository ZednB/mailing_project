from django.urls import path
from blog.views import BlogCreateView, BlogListView, BlogDetailView

urlpatterns = [
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]