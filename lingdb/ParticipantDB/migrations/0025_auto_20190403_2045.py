# Generated by Django 2.1.7 on 2019-04-04 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParticipantDB', '0024_auto_20190306_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaks',
            name='is_native',
            field=models.BooleanField(default=False, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='speaks',
            name='proficiency',
            field=models.CharField(choices=[('NativeLike', 'Native Like'), ('Advanced', 'Advanced'), ('Intermediate', 'Intermediate'), ('Basic', 'Basic')], default='Basic', max_length=11),
        ),
    ]
