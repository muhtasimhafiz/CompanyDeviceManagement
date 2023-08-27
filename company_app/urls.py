from django.urls import path
from . import views

app_name = 'company_app'

urlpatterns = [
    path('register/', views.register_company, name='register_company'),
    path('login/', views.company_login, name='company_login'),
    path('logout/', views.logout_view, name='logout'),
    path('device-logs/', views.device_log_list, name='device_logs'),


    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_device/', views.add_device, name='add_device'),
    path('dashboard/', views.company_dashboard, name='dashboard'),

    path('manage_device/', views.manage_device, name='manage_device'),

]

