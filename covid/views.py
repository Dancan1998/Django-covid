from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from .models import Continent, Country

# Create your views here.


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        continents = Continent.objects.all()
        context = {
            'continents': continents
        }
        return render(request, 'covid/home.html', context)


def countryView(request, pk):
    continents = Continent.objects.all()
    context = {
        'continent': continents
    }
    return render(request, 'covid/continent.html', context)


class CountryView(LoginRequiredMixin, ListView):
    def get(self, request, pk):
        queryset = Continent.objects.get(pk=pk).country_set.all()
        # print(queryset)
        context = {
            'queryset': queryset
        }
        return render(request, 'covid/country.html', context)


class CountryInfoView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return Country.objects.all()
    template_name = 'covid/countryinfo.html'
    context_object_name = 'countinfo'
