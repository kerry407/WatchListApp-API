# Generated by Django 4.1 on 2022-08-28 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0007_watchlist_platform_alter_watchlist_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='platform',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to='watchlist.streamplatform'),
        ),
    ]
