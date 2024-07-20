from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from guesses.models import EmailReminder

class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name",
                  "email", "username", "password1", "password2")

class Edit_SettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name","last_name")
        
class EmailReminderForm(forms.ModelForm):

    class Meta:
        model = EmailReminder
        fields = ("email","subscribe")
        
class LoginEmailForm(forms.Form):
    email = forms.EmailField()


