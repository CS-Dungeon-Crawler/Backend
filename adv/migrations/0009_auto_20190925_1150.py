# Generated by Django 2.2.5 on 2019-09-25 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv', '0008_auto_20190925_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(default='item', max_length=10),
        ),
    ]