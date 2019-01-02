# Generated by Django 2.1 on 2019-01-01 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0002_auto_20181230_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adult',
            name='pref_phone_time',
            field=models.CharField(choices=[('WDM', 'Weekday Mornings'), ('WDA', 'Weekday Afternoons'), ('WDE', 'Weekday Evenings'), ('WEM', 'Weekend Mornings'), ('WEA', 'Weekend Afternoons'), ('WEE', 'Weekend Evenings'), ('ANY', 'Anytime'), ('DNC', 'Do Not Call')], max_length=3, verbose_name='Preferred Phone Time'),
        ),
    ]