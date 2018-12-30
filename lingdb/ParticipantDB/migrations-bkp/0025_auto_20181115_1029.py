# Generated by Django 2.1 on 2018-11-15 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('ParticipantDB', '0024_auto_20181114_1619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adult',
            options={'verbose_name': 'Adult', 'verbose_name_plural': 'Adults'},
        ),
        migrations.AlterModelOptions(
            name='assessment_field',
            options={'verbose_name': 'Assessment Field', 'verbose_name_plural': 'Assessment Fields'},
        ),
        migrations.AlterModelOptions(
            name='assessment_run_field_score',
            options={'verbose_name': 'Assessment Run Field Score', 'verbose_name_plural': 'Assessment Run Field Scores'},
        ),
        migrations.AlterModelOptions(
            name='child',
            options={'verbose_name': 'Child', 'verbose_name_plural': 'Children'},
        ),
        migrations.AlterModelOptions(
            name='experiment',
            options={'verbose_name': 'Experiment', 'verbose_name_plural': 'Experiments'},
        ),
        migrations.AlterModelOptions(
            name='experiment_section_field',
            options={'verbose_name': 'Experiment Section Run', 'verbose_name_plural': 'Experiment Section Runs'},
        ),
        migrations.AlterModelOptions(
            name='isexposedto',
            options={'verbose_name': 'Is Exposed To', 'verbose_name_plural': 'Are Exposed To'},
        ),
        migrations.AlterModelOptions(
            name='lab',
            options={'verbose_name': 'Lab', 'verbose_name_plural': 'Labs'},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Language', 'verbose_name_plural': 'Languages'},
        ),
        migrations.AddField(
            model_name='lab',
            name='field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group'),
        ),
    ]