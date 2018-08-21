# Generated by Django 2.1 on 2018-08-21 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=100)),
                ('preferred_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField()),
                ('gestation_length_weeks', models.SmallIntegerField(blank=True, null=True)),
                ('was_full_term', models.BooleanField(blank=True, null=True)),
                ('birth_weight', models.SmallIntegerField()),
                ('birth_height', models.SmallIntegerField()),
                ('personal_notes', models.TextField(max_length=1000)),
                ('hx_repeated_ear_infection', models.TextField(blank=True, max_length=1000, null=True)),
                ('last_ear_infection', models.DateField(blank=True, null=True)),
                ('hereditary_audio_problems', models.BooleanField()),
                ('hereditary_language_pathologies', models.BooleanField()),
                ('health_notes', models.TextField(blank=True, max_length=1000, null=True)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Langdev_Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Langdev_Experiment_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langdev_experiment_section_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Phono_Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Phono_Experiment_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phono_experiment_section_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.RenameField(
            model_name='adult',
            old_name='yearsOfEducation',
            new_name='years_of_education',
        ),
        migrations.AddField(
            model_name='adult',
            name='preferred_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='adult',
            name='pref_phone_time',
            field=models.CharField(blank=True, choices=[('WDM', 'Weekday Mornings'), ('WDA', 'Weekday Afternoons'), ('WDE', 'Weekday Evenings'), ('WEM', 'Weekend Mornings'), ('WEA', 'Weekend Afternoons'), ('WEE', 'Weekend Evenings'), ('DNC', 'Do Not Call'), ('ANY', 'Anytime')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='adult',
            name='sfu_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
