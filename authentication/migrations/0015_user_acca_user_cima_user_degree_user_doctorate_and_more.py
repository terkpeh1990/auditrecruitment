# Generated by Django 4.2.13 on 2024-05-12 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_user_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='acca',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='cima',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='degree',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='doctorate',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ica',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='masters',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='other',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True),
        ),
    ]