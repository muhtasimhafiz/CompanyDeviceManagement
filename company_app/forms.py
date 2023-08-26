from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee
from .models import Device


class CompanyRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Company Name')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CompanyLoginForm(AuthenticationForm):
    username = forms.CharField(label='Company Name')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user']


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name']
