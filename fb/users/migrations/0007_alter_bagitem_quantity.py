# Generated by Django 4.1.7 on 2023-03-15 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_bag_bagitem_bag_items_bag_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bagitem',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]
