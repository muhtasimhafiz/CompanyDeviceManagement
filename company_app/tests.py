from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Company
from .forms import CompanyRegistrationForm

class RegisterCompanyViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_company_view_post(self):
        # Define test data
        username = 'repliq'
        password = 'admin@3511'

        # Define URL for the register_company view
        url = reverse('company_app:register_company')

        # Simulate a POST request with registration data
        response = self.client.post(url, {'username': username, 'password1': password, 'password2': password})

        # Check if the response status code is 302 (redirect) after successful registration
        self.assertEqual(response.status_code, 302)

        # Check if a new user and company were created
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertTrue(Company.objects.filter(name=username).exists())

    def test_register_company_view_get(self):
        # Define URL for the register_company view
        url = reverse('company_app:register_company')

        # Simulate a GET request
        response = self.client.get(url)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the correct form is used for rendering the template
        self.assertIsInstance(response.context['form'], CompanyRegistrationForm)
