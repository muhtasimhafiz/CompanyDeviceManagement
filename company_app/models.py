from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    # Other fields and methods for Company model

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # Other fields and methods for Employee model

class Device(models.Model):
    name = models.CharField(max_length=100)
    # Other fields and methods for Device model

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    checked_out_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='checkouts')
    checked_in_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='checkins')
    checkout_time = models.DateTimeField()
    checkin_time = models.DateTimeField()
    condition_on_checkout = models.TextField()
    condition_on_checkin = models.TextField()
    # Other fields and methods for DeviceLog model
