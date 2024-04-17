from django.urls import path
from blog.views import BlogCreateView, BlogListView

urlpatterns = [
    path('blog_create/', BlogCreateView.as_view(), name='create_blog'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
]