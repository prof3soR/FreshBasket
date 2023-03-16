# Generated by Django 4.1.7 on 2023-03-14 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_alter_menuitem_quantity_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BagItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.bag')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.menuitem')),
            ],
        ),
        migrations.AddField(
            model_name='bag',
            name='items',
            field=models.ManyToManyField(through='users.BagItem', to='users.menuitem'),
        ),
        migrations.AddField(
            model_name='bag',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
