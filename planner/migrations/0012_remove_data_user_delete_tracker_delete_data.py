# Generated by Django 4.0.3 on 2022-05-11 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0011_delete_item_delete_shoppinglist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='user',
        ),
        migrations.DeleteModel(
            name='Tracker',
        ),
        migrations.DeleteModel(
            name='Data',
        ),
    ]
