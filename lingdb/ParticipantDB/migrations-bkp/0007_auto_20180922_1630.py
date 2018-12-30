# Generated by Django 2.1 on 2018-09-22 23:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0006_auto_20180922_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaks',
            name='age_learning_ended',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='speaks',
            name='age_learning_started',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='speaks',
            name='is_native',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='speaks',
            name='nth_most_dominant',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]