# Generated by Django 2.2.8 on 2019-12-19 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191209_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='account',
            name='cvc',
        ),
        migrations.RemoveField(
            model_name='account',
            name='expiry',
        ),
    ]
