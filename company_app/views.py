from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

from company_app.models import Company
from .forms import *

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            company = Company.objects.create(name=form.cleaned_data['username'])
            company.save()
            return redirect('company_app:dashboard')  
    else:
        form = CompanyRegistrationForm()
    return render(request, 'register.html', {'form': form})

def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('company_app:dashboard')  
    else:
        form = CompanyLoginForm()
    return render(request, 'login.html', {'form': form})

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = request.user.company  # Assign the company to the employee
            employee.save()
            return redirect('company_app:dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def add_device(request):
    # Implement add device view
    pass

def checkout_device(request):
    # Implement device checkout view
    pass

def checkin_device(request):
    # Implement device check-in view
    pass

def company_dashboard(request):
    return render(request, 'dashboard.html')

def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save()
            return redirect('company_app:dashboard')
    else:
        form = DeviceForm()
    return render(request, 'add_device.html', {'form': form})
