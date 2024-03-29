# Generated by Django 4.0.3 on 2022-04-28 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0007_alter_shoppinglist_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('complete', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['complete'],
            },
        ),
        migrations.DeleteModel(
            name='Shopping_List_Item',
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ['list_title']},
        ),
        migrations.RemoveField(
            model_name='shoppinglist',
            name='complete',
        ),
        migrations.RemoveField(
            model_name='shoppinglist',
            name='text',
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='list_title',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='shopping_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.shoppinglist'),
        ),
    ]
