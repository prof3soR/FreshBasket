# Generated by Django 4.1.7 on 2023-03-17 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.CharField(default='0', max_length=50),
            preserve_default=False,
        ),
    ]
