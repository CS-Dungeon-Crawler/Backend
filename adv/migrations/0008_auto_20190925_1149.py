# Generated by Django 2.2.5 on 2019-09-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv', '0007_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(default='', max_length=10),
        ),
    ]
