from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
import requests
User = get_user_model()


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html', {})

    def post(self, request):
        data = request.POST
        context = {
            'data': data,
            'has_error': False,
        }
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        fullname = request.POST.get("name")
        if len(password) < 6:
            messages.add_message(
                request, messages.ERROR, "Passwords should be at least 6 characters long")
            context['has_error'] = True
        if password != password2:
            messages.add_message(
                request, messages.ERROR, "Passwords do not match")
            context['has_error'] = True
        if not validate_email(email, verify=True, check_mx=True):
            messages.add_message(request, messages.ERROR,
                                 "Provide a valid email")
            context['has_error'] = True
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 "Email is already taken")
            context['has_error'] = True
        if User.objects.filter(username=username).exists():
            messages.add_message(
                request, messages.ERROR, "Username is already taken")
            context['has_error'] = True
        if context['has_error']:
            return render(request, 'authentication/register.html', context, status=400)

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.first_name = fullname
        user.last_name = fullname
        user.is_active = False

        user.save()

        current_site = get_current_site(request)
        email_subject = "Activate Your Account"
        message = render_to_string('authentication/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )

        EmailThread(email_message).start()

        messages.add_message(request, messages.SUCCESS,
                             "Account created successfully. Check your email to activate your account")

        return redirect("authentication:login")


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR,
                                 'Invalid login credentials')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'authentication/login.html', status=401, context=context)
        login(request, user)
        return redirect('authentication:home')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Account activated succesfully")
            return redirect("authentication:login")

        return render(request, "authentication/activate_failed.html", status=401)


class HomeView(ListView):
    paginate_by = 10

    def get(self, request):
        response = None
        globalSummary = None
        countries = None
        try:
            response = requests.get('https://api.covid19api.com/summary')
            globalSummary = response.json()['Global']
            countries = response.json()['Countries']
        except ConnectionError as e:
            pass
        context = {
            'globalSummary': globalSummary,
            'countries': countries
        }
        return render(request, "authentication/home.html", context)


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             "Logged out successfully")
        return redirect("authentication:login")


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, "authentication/request-reset-email.html")

    def post(self, request):
        email = request.POST.get("email")

        if not validate_email(email, verify=True, check_mx=True):
            messages.add_message(request, messages.ERROR,
                                 "Provide a valid email")
            return render(request, "authentication/request-reset-email.html")

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = "Reset Your Password"
            message = render_to_string('authentication/reset-user-password.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )

            EmailThread(email_message).start()

        messages.add_message(request, messages.SUCCESS,
                             'We have sent you an email with instructions on how to rest your password')
        return render(request, "authentication/request-reset-email.html")


class SetNewPassword(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.add_message(
                    request, messages.INFO, "Your password reset link has already been used. Request Again")
                return render(request, "authentication/request-reset-email.html")
        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(
                request, messages.INFO, "Your password reset link has already been used. Request Again")
            return render(request, "authentication/request-reset-email.html")
        return render(request, "authentication/set-new-password.html", context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False,
        }
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        fullname = request.POST.get("name")
        if len(password) < 6:
            messages.add_message(
                request, messages.ERROR, "Passwords should be at least 6 characters long")
            context['has_error'] = True
        if password != password2:
            messages.add_message(
                request, messages.ERROR, "Passwords do not match")
            context['has_error'] = True
        if context['has_error']:
            return render(request, "authentication/set-new-password.html", context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.add_message(
                request, messages.SUCCESS, "Your password was reset successfully. You can now login")
            return redirect("authentication:login")
        except DjangoUnicodeDecodeError as identifier:
            messages.add_message(
                request, messages.ERROR, "Something went wrong in resetting your password")
            return render(request, "authentication/set-new-password.html", context)
