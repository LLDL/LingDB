# Generated by Django 2.1 on 2018-12-29 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0008_auto_20181228_1612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lab',
            options={'ordering': ['lab_name'], 'verbose_name': 'Lab', 'verbose_name_plural': 'Labs'},
        ),
        migrations.AlterModelOptions(
            name='musicalskill',
            options={'ordering': ['skill'], 'verbose_name': 'Musical Skill', 'verbose_name_plural': 'Musical Skills'},
        ),
    ]
