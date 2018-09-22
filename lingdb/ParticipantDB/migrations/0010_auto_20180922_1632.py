# Generated by Django 2.1 on 2018-09-22 23:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0009_auto_20180922_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicalexperience',
            name='age_learning_ended',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='musicalexperience',
            name='age_learning_started',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='musicalexperience',
            name='experience',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instrument', to='ParticipantDB.MusicalSkill'),
        ),
        migrations.AlterField(
            model_name='musicalexperience',
            name='nth_most_dominant',
            field=models.SmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]
