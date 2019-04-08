# Generated by Django 2.2 on 2019-04-08 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0026_auto_20190403_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ischildin',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childin', to='ParticipantDB.Child'),
        ),
        migrations.AlterField(
            model_name='ischildin',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c_family', to='ParticipantDB.Family'),
        ),
        migrations.AlterField(
            model_name='isparentin',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='a_family', to='ParticipantDB.Family'),
        ),
    ]
