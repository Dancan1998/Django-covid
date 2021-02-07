from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'covid/home.html')
