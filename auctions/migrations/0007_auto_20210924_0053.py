# Generated by Django 3.2.7 on 2021-09-24 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_amount_bid_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='listing_id',
            new_name='listing',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user_id',
            new_name='user',
        ),
    ]