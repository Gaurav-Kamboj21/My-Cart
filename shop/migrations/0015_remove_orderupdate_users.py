# Generated by Django 2.2.4 on 2020-07-12 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_contact_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderupdate',
            name='users',
        ),
    ]
