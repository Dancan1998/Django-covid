# Generated by Django 3.1.6 on 2021-02-07 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='continent',
            options={'verbose_name_plural': 'Continents'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='coviddata',
            options={'verbose_name_plural': 'CovidData'},
        ),
        migrations.AlterField(
            model_name='country',
            name='hospital_beds_per_thousand',
            field=models.DecimalField(decimal_places=3, max_digits=5),
        ),
    ]
