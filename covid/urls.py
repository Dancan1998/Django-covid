from django.urls import path
from .views import HomeView, CountryView, CountryInfoView
from django.contrib.auth.decorators import login_required

app_name = "covid"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('/<int:pk>', CountryView.as_view(), name="countries"),
    path('country/<int:pk>', CountryInfoView.as_view(), name="country-info"),
]
