# Generated by Django 4.1 on 2022-10-05 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0024_alter_watchlist_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='date_created',
        ),
    ]
