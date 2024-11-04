from django import forms
from .models import Contact
from django.core import validators


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        labels = {'name': "Name", 'email': 'Email', 'message': 'Message'}
        help_text = {'name': 'enter your name'}
        error_messages = {'name': {'required': ' name not mentioned'},
                          'email': {'required': ' email not mentioned'},
                          'message': {'required': ' message not mentioned'}}
