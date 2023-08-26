from django.urls import path
from . import views

app_name = 'company_app'

urlpatterns = [
    path('register/', views.register_company, name='register_company'),
    path('login/', views.company_login, name='company_login'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_device/', views.add_device, name='add_device'),
    path('checkout_device/', views.checkout_device, name='checkout_device'),
    path('checkin_device/', views.checkin_device, name='checkin_device'),
    path('dashboard/', views.company_dashboard, name='dashboard'),
]

