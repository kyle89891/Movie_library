# forms.py
from django import forms


# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class MovieSearchForm(forms.Form):
    query = forms.CharField(label='Search Movies', max_length=100)
