# Generated by Django 5.0 on 2024-01-25 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookApp', '0008_orderbooks_balance_after_transaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooks',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
