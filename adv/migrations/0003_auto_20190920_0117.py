# Generated by Django 2.2.5 on 2019-09-20 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv', '0002_auto_20190920_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='e_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='n_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='s_to',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='w_to',
            field=models.IntegerField(default=0),
        ),
    ]