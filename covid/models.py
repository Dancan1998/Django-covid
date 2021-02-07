from django.db import models
from django_countries.fields import CountryField


class Continent(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Continents'


class Country(models.Model):
    countryyy = CountryField()
    continent = models.ForeignKey(
        Continent, on_delete=models.CASCADE, related_name='continent')
    population = models.IntegerField()
    population_density = models.DecimalField(max_digits=5, decimal_places=3)
    median_age = models.DecimalField(max_digits=5, decimal_places=3)
    aged_65_older = models.DecimalField(max_digits=5, decimal_places=3)
    aged_70_older = models.DecimalField(max_digits=5, decimal_places=3)
    gdp_per_capita = models.DecimalField(max_digits=10, decimal_places=5)
    exteme_poverty = models.DecimalField(
        blank=True, null=True, max_digits=5, decimal_places=3)
    diabetes_prevalence = models.DecimalField(max_digits=8, decimal_places=4)
    female_smokers = models.IntegerField(blank=True, null=True)
    male_smokers = models.IntegerField(blank=True, null=True)
    handwashing_facilities = models.DecimalField(
        max_digits=5, decimal_places=3)
    hospital_beds_per_thousand = models.DecimalField(
        max_digits=5, decimal_places=3)
    life_expectancy = models.DecimalField(max_digits=5, decimal_places=3)
    human_development_index = models.DecimalField(
        max_digits=5, decimal_places=3)
    total_cases = models.IntegerField(default=0)
    new_cases = models.IntegerField(default=0)
    total_deaths = models.IntegerField(default=0)
    new_deaths = models.IntegerField(default=0)
    icu_patients = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.countryyy.name

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['countryyy']


# class CovidData(models.Model):
#     country = models.ForeignKey(
#         Country, on_delete=models.CASCADE, related_name='country')
#     total_cases = models.IntegerField()
#     new_cases = models.IntegerField()
#     total_deaths = models.IntegerField()
#     new_deaths = models.IntegerField()
#     icu_patients = models.IntegerField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name_plural = 'CovidData'
