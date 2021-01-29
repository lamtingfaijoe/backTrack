from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ManagerOrDeveloper

class ManagerOrDeveloperCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    post = forms.ChoiceField(choices=(
		('UD', 'Developer'),
        ('M', 'Manager'),
		))

    class Meta:
        model = ManagerOrDeveloper
        fields = ('username', 'password1', 'password2', 'name', 'post', 'email')

class ManagerOrDeveloperChangeForm(UserChangeForm):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = ManagerOrDeveloper
        fields = ('username', 'password', 'name', 'email')