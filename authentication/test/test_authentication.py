from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("authentication:register")
        self.login_url = reverse("authentication:login")
        self.user = {
            'email': 'dancanchibole8@gmail.com',
            'username': 'danchibole',
            'password': '123456',
            'password2': '123456',
            'name': 'Dan Chibole'
        }

        self.password_not_match = {
            'email': 'dancanchibole8@gmail.com',
            'username': 'danchibole',
            'password': '123456',
            'password2': '12346',
            'name': 'Dan Chibole'
        }

        self.password_length = {
            'email': 'dancanchibole8@gmail.com',
            'username': 'danchibole',
            'password': '12345',
            'password2': '12345',
            'name': 'Dan Chibole'
        }

        self.empy_password = {
            'email': 'dancanchibole8@gmail.com',
            'username': 'danchibole',
            'password': '',
            'password2': '',
            'name': 'Dan Chibole'
        }

        self.inavalid_email = {
            'email': 'admin@gmail.com',
            'username': 'danchibole',
            'password': 'password1234',
            'password2': 'password1234',
            'name': 'Dan Chibole'
        }

        self.empty_email = {
            'email': '',
            'username': 'danchibole',
            'password': '',
            'password2': '',
            'name': 'Dan Chibole'
        }

        self.empty_username_for_login = {
            'username': '',
            'password': '123456',
        }

        self.empty_password_for_login = {
            'username': 'dancanchibole',
            'password': '',
        }

        return super().setUp()


class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 302)

    def test_passwords_dont_match(self):
        response = self.client.post(self.register_url, self.password_not_match)
        self.assertEqual(response.status_code, 400)

    def test_password_length(self):
        response = self.client.post(self.register_url, self.password_length)
        self.assertEqual(response.status_code, 400)

    def test_empty_password(self):
        response = self.client.post(self.register_url, self.password_length)
        self.assertEqual(response.status_code, 400)

    def test_email_exists(self):
        response = self.client.post(self.register_url, self.inavalid_email)
        self.assertEqual(response.status_code, 400)

    def test_email_already_exists(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 400)


class LoginTest(BaseTest):
    def test_can_access_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_can_login_user(self):
        self.client.post(self.register_url, self.user)
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, 302)

    def test_cannot_login_user_without_email_verification(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, 401)

    def test_cannot_login_user_without_username(self):
        response = self.client.post(
            self.login_url, self.empty_username_for_login)
        self.assertEqual(response.status_code, 401)

    def test_cannot_login_user_without_password(self):
        response = self.client.post(
            self.login_url, self.empty_password_for_login)
        self.assertEqual(response.status_code, 401)
