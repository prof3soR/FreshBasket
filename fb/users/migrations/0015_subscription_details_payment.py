# Generated by Django 4.1.7 on 2023-03-29 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_subscription_details_delete_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription_details',
            name='payment',
            field=models.BooleanField(default=False),
        ),
    ]
