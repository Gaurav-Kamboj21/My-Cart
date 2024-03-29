# Generated by Django 2.2.4 on 2020-07-04 19:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200628_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='', max_length=50)),
                ('user_type', models.CharField(choices=[('Seller', 'Seller'), ('Customer', 'Customer')], default='customer', max_length=20)),
                ('user_address', models.TextField()),
                ('user_state', models.CharField(default='India', max_length=50)),
                ('user_city', models.CharField(max_length=50)),
                ('user_Zip', models.CharField(max_length=10)),
                ('user_phone', models.CharField(default='+91', max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='orderupdate',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 4, 19, 0, 40, 776734, tzinfo=utc)),
        ),
    ]
