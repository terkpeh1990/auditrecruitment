# Generated by Django 4.2.13 on 2024-05-13 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0020_user_profesionalbody_user_qualificationtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationalhistory',
            name='attachment',
        ),
        migrations.RemoveField(
            model_name='historicaleducationalhistory',
            name='attachment',
        ),
    ]
