# Generated by Django 3.2.7 on 2021-09-24 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='amount',
            new_name='bid',
        ),
    ]