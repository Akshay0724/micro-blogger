from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Blog


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", required=False)
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2",)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
