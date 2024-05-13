# Generated by Django 4.2.13 on 2024-05-12 14:52

import authentication.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_grade_options_user_city_user_gps_user_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='QualificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'QualificationType',
                'verbose_name_plural': 'QualificationTypes',
                'db_table': 'QualificationType',
                'permissions': [('custom_create_qualification', 'Can Create Qualification')],
            },
        ),
        migrations.CreateModel(
            name='StudyField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'StudyField',
                'verbose_name_plural': 'StudyFields',
                'db_table': 'StudyField',
                'permissions': [('custom_create_field_of_study', 'Can Create StudyField')],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='is_applicant',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='HistoricalStudyField',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical StudyField',
                'verbose_name_plural': 'historical StudyFields',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalQualificationType',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical QualificationType',
                'verbose_name_plural': 'historical QualificationTypes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalEducationalHistory',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('others', models.CharField(max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('completion_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')], max_length=50)),
                ('attachment', models.TextField(max_length=100, validators=[authentication.validators.validate_file_extension])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('qualificationtype', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.qualificationtype')),
                ('studyfield', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.studyfield')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical EducationalHistory',
                'verbose_name_plural': 'historical EducationalHistorys',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='EducationalHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('others', models.CharField(max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
                ('completion_date', models.DateField(null=True)),
                ('status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed')], max_length=50)),
                ('attachment', models.FileField(upload_to='documents/', validators=[authentication.validators.validate_file_extension])),
                ('qualificationtype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_qualification', to='authentication.qualificationtype')),
                ('studyfield', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studyfield', to='authentication.studyfield')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usereducation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'EducationalHistory',
                'verbose_name_plural': 'EducationalHistorys',
                'db_table': 'EducationalHistory',
            },
        ),
    ]