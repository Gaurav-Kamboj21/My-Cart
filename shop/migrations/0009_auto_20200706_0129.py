# Generated by Django 2.2.4 on 2020-07-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200705_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_password',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='user_password2',
            field=models.CharField(default='', max_length=50),
        ),
    ]
