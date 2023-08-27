import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(AbstractUser):
    name = models.CharField(max_length=100)
    # password = models.CharField(default='random_password@3511', max_length=128)
    # username = models.CharField(default='random_name', max_length=128)

    # Other fields and methods for Company model


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    condition_choices = [
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]
    current_condition = models.CharField(max_length=10, choices=condition_choices, default='Good')
    status = models.CharField(max_length=10, choices=[('In', 'In'), ('Out', 'Out')], default='In')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reference_id = models.CharField(unique=True, max_length=10)  
    

    def save(self, *args, **kwargs):
        if not self.reference_id:
            self.reference_id = self.generate_unique_reference_id()
        super().save(*args, **kwargs)
    
    def generate_unique_reference_id(self):
        while True:
                reference_id = self.generate_random_reference_id()
                if not Device.objects.filter(reference_id=reference_id).exists():
                    return reference_id

    def generate_random_reference_id(self):
        import random
        import string
        length = max(4, random.randint(4, 10))
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    checked_out_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='checkouts')
    checkout_time = models.DateTimeField()
    checkin_time = models.DateTimeField(null=True, blank=True)
    condition_on_checkout = models.TextField()
    condition_on_checkin = models.TextField()
