from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from ..models import EmailUser
from django.utils import timezone


class LoginTest(TestCase):
    def setUp(self):
        self.username = 'exampleuser@exampledomain.com'
        self.password = 'zaqmko123321'
        self.user = EmailUser.objects.create_user(self.username, self.password, date_of_birth=timezone.now())

    def test_can_log_in_usinig_default_backend(self):
        self.client.login(email=self.username, password=self.password)
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Logout')
        self.assertContains(response, self.username)

    def test_redirects_to_index_after_correct_login(self):
        self.client.login(email=self.username, password=self.password)
        response = self.client.get('/')
        self.assertRedirects(response, reverse('accounts_profile'))

    def test_can_log_in_using_view(self):
        response = self.client.post(reverse('login'),
                                    {'username': self.username, 'password': self.password, 'remember_me': False},
                                    follow=True)
        self.assertRedirects(response, reverse('accounts_profile'))
        self.assertContains(response, self.username)

    def test_error_message_on_invalid_credentials(self):
        response = self.client.post(reverse('login'),
                                    {'username': 'doesnotexists@host.com', 'password': 'tooweakpassword123',
                                     'remember_me': False},
                                    follow=True)

        self.assertTemplateUsed(response, 'emailuser/login.html')
        self.assertContains(response, 'Invalid email or password')

    def test_help_links_on_the_bottom_of_form(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'emailuser/login.html')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Forgot password?')
