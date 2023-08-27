from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  
from django.contrib.auth.forms import AuthenticationForm
from .models import DeviceLog, Employee
from .models import Device
from .models import Company


class CompanyRegistrationForm(UserCreationForm):
    class Meta:
        model = Company
        fields = ('name','username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['name'].label = 'Company Name'

class CompanyLoginForm(AuthenticationForm):
    username = forms.CharField(label='Company Name')

    class Meta:
        model = Company
        fields = ('username', 'password1', 'password2')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'reference_id']  # Include reference_id in the fields list


class DeviceCheckinForm(forms.Form):
    condition_on_checkin = forms.ChoiceField(choices=Device.condition_choices)
    checked_in_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class DeviceCheckoutForm(forms.Form):
    checked_out_by = forms.ModelChoiceField(queryset=Employee.objects.none())
    # condition_on_checkout = forms.ChoiceField(choices=Device.condition_choices)  # Use the choices from your model
    checked_out_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        instance = kwargs.get('instance')

        super().__init__(*args, **kwargs)
        if company:
            self.fields['checked_out_by'].queryset = Employee.objects.filter(company=company)

    def clean_checked_out_by(self):
        return self.cleaned_data['checked_out_by']
