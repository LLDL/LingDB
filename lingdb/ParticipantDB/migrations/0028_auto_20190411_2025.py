# Generated by Django 2.2 on 2019-04-12 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0027_auto_20190408_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adult',
            name='contact_pref',
            field=models.CharField(blank=True, choices=[('P', 'Phone'), ('E', 'Email')], max_length=1, null=True, verbose_name='Contact Preference'),
        ),
    ]
