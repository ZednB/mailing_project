from django.shortcuts import render
from django.views.generic import CreateView, ListView
from blog.forms import BlogForm
from blog.models import Blog
from django.urls import reverse_lazy
from pytils.translit import slugify


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
