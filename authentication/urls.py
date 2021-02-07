from django.urls import path
from .views import RegisterView, LoginView, ActivateAccountView, HomeView, LogoutView, RequestResetEmailView, SetNewPassword
from django.contrib.auth.decorators import login_required

app_name = "authentication"

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('activate/<uidb64>/<token>',
         ActivateAccountView.as_view(), name="activate"),
    path('setnewpassword/<uidb64>/<token>',
         SetNewPassword.as_view(), name="set-new-password"),
    #     path('', login_required(HomeView.as_view()), name="home"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('request-rest-email', RequestResetEmailView.as_view(),
         name="request-reset-email"),
]
