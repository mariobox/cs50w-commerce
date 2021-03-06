# Generated by Django 3.2.7 on 2021-09-29 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210929_0155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(help_text='Select a category for this listing', null=True, on_delete=django.db.models.deletion.SET_NULL, to='auctions.category'),
        ),
    ]
