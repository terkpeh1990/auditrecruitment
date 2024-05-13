# Generated by Django 4.2.13 on 2024-05-13 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_historicalworkhistory_position_workhistory_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profesionalbody',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofessionalbody', to='authentication.proffesionalbody'),
        ),
        migrations.AddField(
            model_name='user',
            name='qualificationtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userqualification', to='authentication.qualificationtype'),
        ),
    ]
