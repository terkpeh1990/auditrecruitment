# Generated by Django 4.2.13 on 2024-05-11 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_middle_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
