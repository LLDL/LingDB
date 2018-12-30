# Generated by Django 2.1 on 2018-09-20 19:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adult',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=100, verbose_name='Given Name')),
                ('preferred_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Preferred Name')),
                ('surname', models.CharField(default='', max_length=100, verbose_name='Surname')),
                ('birth_date', models.DateField(verbose_name='Birth Date')),
                ('gender', models.CharField(default='', max_length=100)),
                ('sfu_id', models.IntegerField(blank=True, null=True, verbose_name='SFU ID')),
                ('address', models.CharField(max_length=200)),
                ('years_of_education', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Years of Education')),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_pref', models.CharField(choices=[('P', 'Phone'), ('E', 'Email')], max_length=1, verbose_name='Contact Preference')),
                ('pref_phone_time', models.CharField(choices=[('WDM', 'Weekday Mornings'), ('WDA', 'Weekday Afternoons'), ('WDE', 'Weekday Evenings'), ('WEM', 'Weekend Mornings'), ('WEA', 'Weekend Afternoons'), ('WEE', 'Weekend Evenings'), ('ANY', 'Anytime'), ('DNC', 'Do Not Call')], default='DNC', max_length=3, verbose_name='Preferred Phone Time')),
                ('health_notes', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Health Notes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('assessment_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('flex_1_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_1_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_1_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_2_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_3_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_4_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_5_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_6_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_max_value', models.SmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assessment_Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField(max_length=1000)),
                ('assessor', models.TextField(max_length=100)),
                ('flex_1_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_score', models.SmallIntegerField(blank=True, null=True)),
                ('adult_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Adult')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Assessment')),
            ],
            options={
                'verbose_name': 'Assessment Run',
                'verbose_name_plural': 'Assessment Runs',
            },
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('given_name', models.CharField(max_length=100, verbose_name='Given Name')),
                ('preferred_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Preferred Name')),
                ('surname', models.CharField(default='', max_length=100, verbose_name='Surname')),
                ('birth_date', models.DateField(verbose_name='Birth Date')),
                ('gender', models.CharField(default='', max_length=100)),
                ('gestation_length_weeks', models.SmallIntegerField(blank=True, null=True, verbose_name='Gestation Length (Weeks)')),
                ('was_full_term', models.BooleanField(blank=True, null=True, verbose_name='Was Full Term?')),
                ('birth_weight', models.SmallIntegerField(blank=True, null=True, verbose_name='Birth Weight (Grams)')),
                ('birth_height', models.SmallIntegerField(blank=True, null=True, verbose_name='Birth Height (CM)')),
                ('personal_notes', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Personal Notes')),
                ('hx_repeated_ear_infection', models.TextField(blank=True, max_length=1000, null=True, verbose_name='HX of Repeated Ear Infection')),
                ('last_ear_infection', models.DateField(blank=True, null=True, verbose_name='Last Ear Infection')),
                ('hereditary_audio_problems', models.BooleanField(verbose_name='Hereditary Audio Problems?')),
                ('hereditary_language_pathologies', models.BooleanField(verbose_name='Hereditary Language Pathologies?')),
                ('health_notes', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Health Notes')),
            ],
            options={
                'verbose_name_plural': 'Children',
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('experiment_name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Experiment Name')),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_section_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('prep', 'In Prep'), ('recruiting', 'Actively Recruiting'), ('inactive', 'Inactive')], max_length=10)),
                ('flex_1_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_1_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_1_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_2_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_3_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_4_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_5_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_name', models.CharField(blank=True, max_length=100, null=True)),
                ('flex_6_min_value', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_max_value', models.SmallIntegerField(blank=True, null=True)),
                ('section_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Experiment')),
            ],
            options={
                'verbose_name': 'Experiment Section',
                'verbose_name_plural': 'Experiment Sections',
            },
        ),
        migrations.CreateModel(
            name='Experiment_Section_Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField(max_length=1000)),
                ('assessor', models.TextField(max_length=100)),
                ('flex_1_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_2_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_3_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_4_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_5_score', models.SmallIntegerField(blank=True, null=True)),
                ('flex_6_score', models.SmallIntegerField(blank=True, null=True)),
                ('adult_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Adult')),
                ('child_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Child')),
                ('experiment_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Experiment_Section')),
            ],
            options={
                'verbose_name': 'Experiment Section Run',
                'verbose_name_plural': 'Experiment Section Runs',
            },
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Family',
                'verbose_name_plural': 'Families',
            },
        ),
        migrations.CreateModel(
            name='IsChildIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Child')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Family')),
            ],
            options={
                'verbose_name': 'Is Child In',
                'verbose_name_plural': 'Are Children In',
            },
        ),
        migrations.CreateModel(
            name='IsExposedTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage_exposure', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('child', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Child')),
            ],
            options={
                'verbose_name_plural': 'Is Exposed To',
            },
        ),
        migrations.CreateModel(
            name='IsParentIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Family')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Adult')),
            ],
            options={
                'verbose_name': 'Is Parent In',
                'verbose_name_plural': 'Are Parents In',
            },
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('lab_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('language_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Musical_Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nth_most_dominant', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('age_learning_started', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('age_learning_ended', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
            ],
            options={
                'verbose_name_plural': 'Musical Experiences',
            },
        ),
        migrations.CreateModel(
            name='Musical_Skill',
            fields=[
                ('skill', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Speaks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_native', models.BooleanField()),
                ('nth_most_dominant', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('age_learning_started', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('age_learning_ended', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)])),
                ('language', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='languagespoken', to='ParticipantDB.Language')),
                ('person', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='speaker', to='ParticipantDB.Adult')),
            ],
            options={
                'verbose_name_plural': 'Speaks',
            },
        ),
        migrations.AddField(
            model_name='musical_experience',
            name='experience',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='instrument', to='ParticipantDB.Musical_Skill'),
        ),
        migrations.AddField(
            model_name='musical_experience',
            name='person',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='musician', to='ParticipantDB.Adult'),
        ),
        migrations.AddField(
            model_name='isexposedto',
            name='language',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Language'),
        ),
        migrations.AddField(
            model_name='family',
            name='children',
            field=models.ManyToManyField(through='ParticipantDB.IsChildIn', to='ParticipantDB.Child'),
        ),
        migrations.AddField(
            model_name='family',
            name='parents',
            field=models.ManyToManyField(through='ParticipantDB.IsParentIn', to='ParticipantDB.Adult'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Lab'),
        ),
        migrations.AddField(
            model_name='child',
            name='exposed_to',
            field=models.ManyToManyField(default=None, through='ParticipantDB.IsExposedTo', to='ParticipantDB.Language', verbose_name='Languages Exposed To'),
        ),
        migrations.AddField(
            model_name='assessment_run',
            name='child_participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Child'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ParticipantDB.Lab'),
        ),
        migrations.AddField(
            model_name='adult',
            name='languages',
            field=models.ManyToManyField(blank=True, through='ParticipantDB.Speaks', to='ParticipantDB.Language'),
        ),
        migrations.AddField(
            model_name='adult',
            name='musical_background',
            field=models.ManyToManyField(blank=True, through='ParticipantDB.Musical_Experience', to='ParticipantDB.Musical_Skill'),
        ),
    ]