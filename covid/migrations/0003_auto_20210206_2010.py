# Generated by Django 3.1.6 on 2021-02-07 04:10

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0002_auto_20210206_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
