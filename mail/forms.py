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
        exclude = ('owner',)


class ModeratorNewsletterForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ('status',)


class MessageForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormsMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)

