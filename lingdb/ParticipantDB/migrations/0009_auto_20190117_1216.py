# Generated by Django 2.1 on 2019-01-17 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0008_auto_20190117_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isparentin',
            name='isPrimary',
            field=models.BooleanField(default=False, verbose_name='Primary Contact?'),
        ),
    ]
