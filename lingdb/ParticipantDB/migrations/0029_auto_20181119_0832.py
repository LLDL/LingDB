# Generated by Django 2.1 on 2018-11-19 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0028_auto_20181119_0828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experiment_section',
            old_name='part_of',
            new_name='experiment',
        ),
    ]
