# Generated by Django 2.1.7 on 2019-04-04 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0025_auto_20190403_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaks',
            name='proficiency',
            field=models.CharField(choices=[('Native', 'Native Like'), ('Advanced', 'Advanced'), ('Intermediate', 'Intermediate'), ('Basic', 'Basic')], default='Basic', max_length=11),
        ),
    ]
