# Generated by Django 4.1.7 on 2023-03-17 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_bagitem_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='DroppedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
