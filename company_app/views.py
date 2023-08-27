import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm

from company_app.models import Company
from .forms import *

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create the user instance but don't save it yet
            user.username = form.cleaned_data['username']  # Set the username from the form
            user.save()  # Save the user instance
            login(request, user)
            company_name = form.cleaned_data['name']
            company = Company.objects.create(name=company_name)
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
            employee.company_id = request.user.id
            employee.save()
            return redirect('company_app:dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.company_id = request.user.id 
            device.save()
            return redirect('company_app:dashboard')
    else:
        form = DeviceForm()
    return render(request, 'add_device.html', {'form': form})




def company_dashboard(request):
    employees = Employee.objects.filter(company=request.user)
    devices = Device.objects.filter(company=request.user)

    context = {
        'employees': employees,
        'devices': devices,
    }
    return render(request, 'dashboard.html', context)

def manage_device(request):
    devices = Device.objects.filter(company=request.user)
    for device in devices:
        try:
            latest_log = device.devicelog_set.latest('checkout_time')
            device.logs = {
                'log': latest_log,
                'checked_out_by': latest_log.checked_out_by if latest_log.checked_out_by else None,
                'checked_out_by_id': latest_log.checked_out_by.id,
                'checkout_time':latest_log.checkout_time

            }
        except DeviceLog.DoesNotExist:
            device.logs = None
        
    if request.method == 'POST':
        if 'checkout' in request.POST:
            checkout_form = DeviceCheckoutForm(request.POST, company=request.user)
            checkin_form = DeviceCheckinForm()  

            if checkout_form.is_valid():
                device_id = request.POST.get('device_id')
                device = get_object_or_404(Device, id=device_id)

                checked_out_by = checkout_form.cleaned_data['checked_out_by']
                # condition_on_checkout = checkout_form.cleaned_data['condition_on_checkout']
                checked_out_at = checkout_form.cleaned_data['checked_out_at']

                # device.current_condition = condition_on_checkout
                device.status = 'Out'
                device.save()

                log = DeviceLog.objects.create(
                    device=device,
                    company=request.user,
                    checked_out_by=checked_out_by,
                    checkout_time=checked_out_at,
                    condition_on_checkout=device.current_condition
                )

        elif 'checkin' in request.POST:
            checkout_form = DeviceCheckoutForm(company=request.user)
            checkin_form = DeviceCheckinForm(request.POST)

            if checkin_form.is_valid():
                device_id = request.POST.get('device_id')
                device = get_object_or_404(Device, id=device_id)

                condition_on_checkin = checkin_form.cleaned_data['condition_on_checkin']
                checkin_time = checkin_form.cleaned_data['checked_in_at']


                log = DeviceLog.objects.get(device=device, checkin_time=None)
                log.condition_on_checkin = condition_on_checkin
                log.checkin_time = checkin_time
                log.save()

                device.current_condition = condition_on_checkin
                device.status = 'In'
                device.save()

        else:
            print('Checkout form errors:', checkout_form.errors)
            print('Checkin form errors:', checkin_form.errors)

        return redirect('company_app:manage_device')
    else:
        checkout_form = DeviceCheckoutForm(company=request.user)
        checkin_form = DeviceCheckinForm()

    context = {
        'devices': devices,
        'checkout_form': checkout_form,
        'checkin_form': checkin_form
    }

    return render(request, 'manage_device.html', context)


def logout_view(request):
    logout(request)
    return redirect('company_app:company_login')  

def device_log_list(request):
    logs = DeviceLog.objects.all().order_by('-checkout_time') 
    context = {'logs': logs}
    return render(request, 'device_log_list.html', context)
