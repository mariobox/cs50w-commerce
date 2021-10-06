# Generated by Django 3.2.7 on 2021-09-29 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_favorite_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a category (e.g. Books)', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(help_text='Select a category for this listing', to='auctions.Category'),
        ),
    ]