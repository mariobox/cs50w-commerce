# Generated by Django 3.2.7 on 2021-09-24 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210924_0053'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='bid',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user',
            new_name='owner',
        ),
    ]
