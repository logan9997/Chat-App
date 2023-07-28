from django import forms
from .config import NAME_MAX_LENGTH

class Login(forms.Form):
    name = forms.CharField(max_length=NAME_MAX_LENGTH)