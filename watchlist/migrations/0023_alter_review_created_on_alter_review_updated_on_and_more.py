# Generated by Django 4.1 on 2022-10-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0022_alter_review_created_on_alter_review_updated_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
