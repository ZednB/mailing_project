from django import forms
from mail.models import NewsLetter, Message, Client


class StyleFormsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'


class MessageForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

