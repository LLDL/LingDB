# Generated by Django 2.1 on 2019-02-13 00:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0010_auto_20190117_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adult',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='adult',
            name='pref_phone_time',
            field=models.CharField(blank=True, choices=[('WDM', 'Weekday Mornings'), ('WDA', 'Weekday Afternoons'), ('WDE', 'Weekday Evenings'), ('WEM', 'Weekend Mornings'), ('WEA', 'Weekend Afternoons'), ('WEE', 'Weekend Evenings'), ('ANY', 'Anytime'), ('DNC', 'Do Not Call')], default='ANY', max_length=3, null=True, verbose_name='Preferred Phone Time'),
        ),
        migrations.AlterField(
            model_name='adult',
            name='years_of_education',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Years of Education'),
        ),
    ]
