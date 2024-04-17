from django import forms

from blog.models import Blog


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('create_date', 'view_count',)
