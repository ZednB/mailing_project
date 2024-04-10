from django import forms
from mail.models import NewsLetter


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ('scheduled_time', 'frequency')
