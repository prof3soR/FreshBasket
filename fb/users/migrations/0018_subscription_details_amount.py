# Generated by Django 4.2 on 2023-04-12 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_subscription_details_area_street_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription_details',
            name='amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
