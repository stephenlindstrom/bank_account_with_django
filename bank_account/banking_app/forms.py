from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from banking_app.models import Account, Organization, Membership

class DepositForm(forms.Form):
    deposit_amount = forms.DecimalField(min_value=0, decimal_places=2)

class WithdrawForm(forms.Form):
    withdraw_amount = forms.DecimalField(min_value=0, decimal_places=2)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name']

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name']
        labels = {'name': ('Group name'),}