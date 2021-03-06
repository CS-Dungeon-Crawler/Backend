# Generated by Django 2.2.5 on 2019-09-25 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adv', '0005_room_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='adv.Item')),
                ('armor_value', models.IntegerField(default=1)),
            ],
            bases=('adv.item',),
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='adv.Item')),
                ('damage', models.IntegerField(default=8)),
            ],
            bases=('adv.item',),
        ),
        migrations.AddField(
            model_name='item',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
